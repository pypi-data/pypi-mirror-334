## 0.0.2 (2025-03-15)


- resolve border width from config or actual window
    - as opposed to hard-coded config
- store & hyrdrate shell ratios on i3 restart
- remove [--toggle] option
- only decrease the window width by 2*border_width
  if we have more than one active output


## 0.0.1 (2025-03-13)


- start using CI
- pull in some changes from upstream
    - move config file location to ~/.config/i3-quickterm/config.json
    - add 'auto' term option
- add support for toggling shell via process signals
- add singleton lock for daemon process
