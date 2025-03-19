#!/usr/bin/env python3

import socket
import sys
import json
import os
import argparse
from contextlib import contextmanager, suppress

import fcntl
import shlex
import subprocess

from pathlib import Path
from math import isclose

import i3ipc
import selectors
import signal
import shutil
from datetime import datetime
from i3_quickterm.version import __version__

CONF = {  # define default values here; can be overridden by user conf
    "menu": "rofi -dmenu -p 'quickterm: ' -no-custom -auto-select",
    "term": "auto",
    "history": "{$HOME}/.cache/i3-quickterm/shells.order",
    "socket": "/tmp/.i3-quickterm.sock",
    "state_f": "/tmp/.i3-quickterm.state",
    "max_persisted_state_age_sec": 2,
    "store_state_on_restart": True,
    "ratio": 0.25,
    "borderWidthPx": -1,  # value will be resolved at init; if you don't want border value to be found from config, set it to value >= 0
    "defaultBorderWidthPx": 2,  # default/fallback value; we try to fetch actual value from config
    "pos": "top",
    "shells": {
        "haskell": "ghci",  # TODO: removed from upstream
        "js": "node",
        "python": "ipython3 --no-banner --no-confirm-exit",
        "shell": "{$SHELL}"
    },
    "signalToShellToggles": {
        "SIGUSR1": "shell"
    },
    "envVarBlacklistPatterns": [],
    "envVarBlacklist": []
}

SHELL_RATIOS = {}  # will be initialized on init
MARK_QT_PATTERN = 'quickterm_.*'
MARK_QT = 'quickterm_{}'


def TERM(executable, execopt='-e', execfmt='expanded', titleopt='-T'):
    """Helper to declare a terminal in the hardcoded list"""
    if execfmt not in ('expanded', 'string'):
        raise RuntimeError('Invalid execfmt')

    fmt = executable

    if titleopt is not None:
        fmt += ' ' + titleopt + ' {title}'

    fmt += f" {execopt} {{{execfmt}}}"
    return fmt

TERMS = {
    'alacritty': TERM('alacritty', titleopt='-t'),
    'foot': TERM('foot', titleopt='-T', execopt='', execfmt='expanded'),
    'gnome-terminal': TERM('gnome-terminal', execopt='--', titleopt=None),
    'kitty': TERM('kitty', titleopt='-T'),
    'roxterm': TERM('roxterm'),
    'st': TERM('st'),
    'terminator': TERM('terminator', execopt='-x', titleopt='-T'),
    'termite': TERM('termite', execfmt='string', titleopt='-t'),
    'urxvt': TERM('urxvt'),
    'urxvtc': TERM('urxvtc'),
    'xfce4-terminal': TERM('xfce4-terminal', execfmt='string'),
    'xterm': TERM('xterm'),
}


def quoted(s):
    return "'" + s + "'"


def expand_command(cmd, **rplc_map):
    d = {'$' + k: v for k, v in os.environ.items()}
    d.update(rplc_map)
    return shlex.split(cmd.format(**d))


def term_title(shell):
    return '{} - i3-quickterm'.format(shell)


def conf_path():
    home_dir = os.environ['HOME']
    xdg_dir = os.environ.get('XDG_CONFIG_DIR', '{}/.config'.format(home_dir))
    return xdg_dir + '/i3-quickterm/config.json'


def read_conf():
    try:
        with open(conf_path(), 'r') as f:
            return json.load(f)
    except Exception as e:
        print('invalid config file: {}'.format(e), file=sys.stderr)
        return {}


@contextmanager
def get_history_file():
    if CONF['history'] is None:
        yield None
        return

    p = Path(expand_command(CONF['history'])[0])
    os.makedirs(str(p.parent), exist_ok=True)

    f = open(str(p), 'a+')
    fcntl.lockf(f, fcntl.LOCK_EX)

    try:
        f.seek(0)
        yield f
    finally:
        fcntl.lockf(f, fcntl.LOCK_UN)
        f.close()


def load_conf():
    CONF.update(read_conf())


def move_to_scratchpad(conn, selector):
    conn.command('{} floating enable, move scratchpad'
                 .format(selector))


# make terminal visible
def focus_on_current_ws(conn, mark_name, ratio=0.25, border_width=0):
    ws = get_current_workspace(conn)
    wx, wy = ws.rect.x, ws.rect.y
    width = ws.rect.width
    if CONF['OUTPUTS'] > 1:
        width -= border_width*2  # decrease twice the window border width, otherwise the window won't fit on the screen, and overflows into neighbouring screen
    wheight = ws.rect.height

    height = int(wheight * ratio)
    posx = wx

    if CONF['pos'] == 'bottom':
        margin = 6
        posy = wy + wheight - height - margin
    else:  # pos == 'top'
        posy = wy

    conn.command('[con_mark={mark}],'
                 'move scratchpad,'
                 'scratchpad show,'
                 'resize set {width} px {height} px,'
                 'move absolute position {posx}px {posy}px'
                 ''.format(mark=mark_name, posx=posx, posy=posy,
                           width=width, height=height))


def get_current_workspace(conn):
    return conn.get_tree().find_focused().workspace()


def toggle_quickterm_select():
    """Hide a quickterm visible on current workspace or prompt
    the user for a shell type"""
    conn = i3ipc.Connection()

    # TODO: does this first block need to exist? e.g. if we already have a py shell
    #       open & we execute qt w/o arguments again, it'll just hide it instead of
    #       prompting us for shell to open.

    # is there a quickterm opened in the current workspace?
    qt = get_current_workspace(conn).find_marked(MARK_QT_PATTERN)
    if qt:
        qt = qt[0]
        move_to_scratchpad(conn, '[con_id={}]'.format(qt.id))
        return

    # undefined shell and nothing on workspace: ask for shell selection
    with get_history_file() as hist:
        # compute the list from conf + (maybe) history
        hist_list = None
        if hist is not None:
            with suppress(Exception):
                hist_list = json.load(hist)

                # invalidate if different set from the configured shells
                if set(hist_list) != set(CONF['shells'].keys()):
                    hist_list = None

        shells = hist_list or sorted(CONF['shells'].keys())

        proc = subprocess.Popen(expand_command(CONF['menu']),
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE)

        assert proc.stdin is not None

        for r in shells:
            proc.stdin.write((r + '\n').encode())
        stdout, _ = proc.communicate()

        shell = stdout.decode().strip()

        if len(shell) == 0:
            return
        elif shell not in CONF['shells']:
            return

        if hist is not None:
            # put the selected shell on top
            shells = [shell] + [s for s in shells if s != shell]
            hist.truncate(0)
            json.dump(shells, hist)
    send_msg(shell)


def select_terminal():
    t = CONF['term']
    if t == 'auto':
        for t, fmt in sorted(TERMS.items()):
            if shutil.which(t) is not None:
                return fmt
        raise RuntimeError(
            f"Could not find a suitable terminal "
            f"in the predefined list: {sorted(TERMS.keys())}"
        )

    if t in TERMS:
        # one of the pre-configured terminals
        return TERMS.get(t)

    return t


def toggle_quickterm(shell, conn):
    shell_mark = MARK_QT.format(shell)
    qt = conn.get_tree().find_marked(shell_mark)

    # does it exist already?
    if len(qt) == 0:
        # print('qt wind does not exist')
        term = select_terminal()
        qt_cmd = "{} -i -r {} -b {} -o {} {}".format(sys.argv[0],
                                                    SHELL_RATIOS[shell],
                                                    CONF['borderWidthPx'],
                                                    CONF['OUTPUTS'],
                                                    shell)

        term_cmd = expand_command(term, title=quoted(term_title(shell)),
                                  expanded=qt_cmd,
                                  string=quoted(qt_cmd))
        #os.execvp(term_cmd[0], term_cmd)  # note we can't do execvp() with server paradigm, as it'd replace our daemon process
        subprocess.Popen(term_cmd)
    else:  # qt window already exists
        # print('qt wind exists')
        qt = qt[0]

        if qt.workspace().name == get_current_workspace(conn).name:
            # print('  moving win back')
            current_ratio = qt.rect.height / qt.workspace().rect.height
            # note we also don't want to store ratio if we're fullscreen:
            if qt.fullscreen_mode != 1 and not isclose(current_ratio, SHELL_RATIOS[shell], abs_tol=0.01):
                SHELL_RATIOS[shell] = current_ratio
            move_to_scratchpad(conn, '[con_id={}]'.format(qt.id))
        else:
            # print('  bringing win up')
            focus_on_current_ws(conn, shell_mark, SHELL_RATIOS[shell], qt.current_border_width)


# before running the shell process in-place, remove blacklisted environment variables:
def clean_env():
    blacklistedEnvVars = CONF.get('envVarBlacklistPatterns')
    if blacklistedEnvVars:
        from re import compile
        blacklistedEnvVars = [compile(i) for i in blacklistedEnvVars]
        for k, v in os.environ.items():
            for blacklistRgx in blacklistedEnvVars:
                if blacklistRgx.fullmatch(k):
                    os.environ.pop(k, None)
                    break

    for env_var in CONF.get('envVarBlacklist', []):
        os.environ.pop(env_var, None)


# note instead of passing border value here, we could resolve it ourselves
# by    border = find_border_width(conn)
def launch_inplace(shell, ratio, border, outputs):
    """QT is called by itself
       Mark current window, move back and focus again, then run shell in current process
    """
    conn = i3ipc.Connection()
    shell_mark = MARK_QT.format(shell)
    qt = conn.get_tree().find_marked(shell_mark)
    if not qt:
        conn.command('mark {}'.format(shell_mark))
        # move_to_scratchpad(conn, '[con_mark={}]'.format(shell_mark))  # was removed by upstream as unneeded; haven't confirmed myself
        CONF['OUTPUTS'] = outputs
        focus_on_current_ws(conn, shell_mark, ratio, border)

    prog_cmd = expand_command(CONF['shells'][shell])
    clean_env()
    os.execvp(prog_cmd[0], prog_cmd)


def _unix_time_now() -> int:
    return int(datetime.now().timestamp())


def persist_state():
    try:
        data = {
                'timestamp': _unix_time_now(),
                'ratios': SHELL_RATIOS
               }

        with open(CONF['state_f'], 'w') as f:
            json.dump(data, f)
    except Exception as e:
        print(e)


def load_ratios() -> dict:
    default = {k: CONF['ratio'] for k in set(CONF['shells'].keys())}

    ff = CONF['state_f']
    if not (os.path.isfile(ff) and os.access(ff, os.R_OK)):
        return default

    try:
        with open(ff, 'r') as f:
            s = json.load(f)
            t = s.get('timestamp', 0)

            if (_unix_time_now() - t <= CONF['max_persisted_state_age_sec']):
                return s.get('ratios', default)
    except Exception as e:
        print(e)
    return default


def on_shutdown(i3, e):
    if e.change == 'restart' and CONF['store_state_on_restart']:
        persist_state()
    os._exit(0)


def on_output(i3, e=None):
    CONF['OUTPUTS'] = len([o for o in i3.get_outputs() if o.active])


# equivalent to:
# i3-msg -r -t get_config | jq -r '.included_configs[].variable_replaced_contents' | grep -Po '^default_border\s+.*\s+\K\d+$'
def find_border_width(conn):
    v = CONF['borderWidthPx']
    if v > -1:
        return v

    try:
        c = conn.get_config()
        v = next(x for x in c.ipc_data['included_configs'][0]['variable_replaced_contents'].split('\n') if x.startswith('default_border '))
        return int(v.split()[-1])
    except Exception as e:
        return CONF['defaultBorderWidthPx']


class Listener:
    def __init__(self):
        self.i3 = i3ipc.Connection()
        CONF['borderWidthPx'] = find_border_width(self.i3)
        on_output(self.i3)
        self.i3.on('shutdown', on_shutdown)
        self.i3.on('output', on_output)
        self.listening_socket = socket.socket(socket.AF_UNIX,
                                              socket.SOCK_STREAM)
        sock = CONF['socket']

        if os.path.exists(sock):
            os.remove(sock)
        self.listening_socket.bind(sock)
        self.listening_socket.listen(1)

    def launch_i3(self):
        self.i3.main()

    def launch_server(self):
        selector = selectors.DefaultSelector()

        def accept(sock):
            conn, addr = sock.accept()
            selector.register(conn, selectors.EVENT_READ, read)

        def read(conn):
            data = conn.recv(16)
            if not data:
                selector.unregister(conn)
                conn.close()
            elif len(data) > 0:
                shell = data.decode().strip()
                self.toggle(shell)

        selector.register(self.listening_socket, selectors.EVENT_READ, accept)

        while True:
            for key, event in selector.select():
                callback = key.data
                callback(key.fileobj)

    def run(self):
        from threading import Thread

        t_i3 = Thread(target=self.launch_i3)
        t_server = Thread(target=self.launch_server)
        for t in (t_i3, t_server):
            t.start()

    def toggle(self, shell):
        toggle_quickterm(shell, self.i3)


def send_msg(shell):
    client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client_socket.connect(CONF['socket'])
    client_socket.send(shell.encode())
    client_socket.close()


def validate_shell_arg(shell):
    if shell not in CONF['shells']:
        print('unknown shell: {}'.format(shell), file=sys.stderr)
        return False
    return True


def main():
    parser = argparse.ArgumentParser(prog='i3-quickterm',
                                     description="""
        Launch and toggle the visibility of shells.

        --daemon option launches the daemon process; it's required to
        keep stateful information, such as per-shell height ratio.
        """)
    parser.add_argument('-d', '--daemon',
                        dest='daemon',
                        help='start the daemon',
                        action='store_true')
    parser.add_argument('-i', '--in-place',
                        dest='in_place',
                        action='store_true')
    parser.add_argument('-r', '--ratio',
                        dest='ratio',
                        type=float,
                        help='height ratio of a shell to be instantiated')
    parser.add_argument('-b', '--border',
                        dest='border',
                        type=int,
                        help='assumed border width of the window to be instantiated')
    parser.add_argument('-o', '--outputs',
                        dest='outputs',
                        type=int,
                        help='number of active monitors')

    parser.add_argument('shell', metavar='SHELL', nargs='?')
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    args = parser.parse_args()

    load_conf()

    if args.daemon:
        from tendo import singleton

        global LOCK
        LOCK = singleton.SingleInstance()
        global SHELL_RATIOS
        SHELL_RATIOS = load_ratios()

        listener = Listener()
        listener.run()

        for sig, shell in CONF['signalToShellToggles'].items():
            signal.signal(getattr(signal, sig), lambda s, stack_frame: listener.toggle(shell))
    elif args.shell is None:
        toggle_quickterm_select()
        sys.exit(0)
    elif not validate_shell_arg(args.shell):
        sys.exit(1)
    elif args.in_place:
        launch_inplace(args.shell, args.ratio, args.border, args.outputs)
    else:  # toggle shell
        send_msg(args.shell)


if __name__ == '__main__':
    main()
