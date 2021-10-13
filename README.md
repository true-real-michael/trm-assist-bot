# trm-assist-bot

Simple Telegram bot for interacting with the PC remotely from a mobile device.

Currently comprises a single module, that is used for controlling media (volume, play/pause, scroll)

### Preparing
install libraries:
- `python-telegram-bot`
- `pyautogui`

in `config.py`:
- add your telegram id to `ADMINS`, otherwise the bot won't let you perform some (currently, all) actions
- assign a valid bot token to `TOKEN`

### Usage
Send `/start` to initiate conversation or return to the main menu.
Use inline keyboards to navigate through menus and interact with them.
