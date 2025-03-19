# i3-quickterm

A small drop-down terminal for [i3wm](https://i3wm.org/) and [sway](https://swaywm.org/)

Note this is a fork of [lbonn/i3-quickterm](https://github.com/lbonn/i3-quickterm).
Upstream is still active and maintained, but the fork you're currently viewing
has somewhat diverged in its architecture -- mainly started employing client-server
paradigm.

## Features

* use your favourite terminal emulator
* can select a shell with [dmenu](http://tools.suckless.org/dmenu/) /
  [rofi](https://github.com/davatorium/rofi)
* adapt to screen width
* multi-monitor aware

## Installation

```
pipx install i3-qt
```

## Usage

When launched, it will minimize the quickterm on the current screen if there is
one.  Otherwise, it will either prompt the user for the shell to open or use the
one supplied in argument.

If the requested shell is already opened on another screen, it will be moved on
the current screen.

First a daemon process needs to be started:

```
exec_always --no-startup-id i3-quickterm --daemon
```

It is recommended to map it to an i3 binding:

```
# with prompt:
bindsym $mod+p exec --no-startup-id i3-quickterm
# ...or always pop standard shell, without the selection menu:
bindsym $mod+b exec --no-startup-id i3-quickterm shell
```

## Configuration

The configuration is read from `~/.config/i3-quickterm/config.json`

* `menu`: the dmenu-compatible application used to select the shell
* `term`: the terminal emulator of choice
* `history`: a file to save the last-used shells order, last-used ordering
  is disabled if set to null
* `ratio`: the initial percentage of the screen height to use
* `borderWidthPx`: the window border width configured in i3
* `pos`: where to pop the terminal (`top` or `bottom`)
* `shells`: registered shells (`{ name: command }`)

`term` can be either:
- a format string, like this one: `urxvt -t {title} -e {expanded}` with
  the correct arguments format of your terminal. Some terminals - like
  xfce4-terminal - need the command argument to be passed as a string. In
  this case, replace `{expanded}` by `{string}`
- `auto` to select the first existing terminal of the list above (only to
  provide friendler defaults, not recommended otherwise)
- a terminal name from the hardcoded list, which should work out of the box.
  Right now, the only reference for the list is the source code
  (search for `TERMS =`).
  If you'd like to add another terminal (or correct an error), please open
  a pull request.

`menu`, `term`, `history` and `shell` can contain placeholders for environment
variables: `{$var}`.

Unspecified keys are inherited from the defaults:

```
{
    "menu": "rofi -dmenu -p 'quickterm: ' -no-custom -auto-select",
    "term": "auto",
    "history": "{$HOME}/.cache/i3-quickterm/shells.order",
    "socket": "/tmp/.i3-quickterm.sock",
    "ratio": 0.25,
    "borderWidthPx": 2,
    "pos": "top",
    "shells": {
        "haskell": "ghci",  # TODO: removed from upstream
        "js": "node",
        "python": "ipython3 --no-banner",
        "shell": "{$SHELL}"
    },
    "signalToShellToggles": {
        "SIGUSR1": "shell"
    },
    "envVarBlacklistPatterns": [],
    "envVarBlacklist": []
}
```

## Requirements

* python >= 3.8
* i3 >= v3.11 or sway >= 1.2
* [i3ipc-python](https://i3ipc-python.readthedocs.io/en/latest/) >= v2.0.1
* dmenu or rofi (optional)
