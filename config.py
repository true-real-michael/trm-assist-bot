# Needs a valid Telegram Bot Token to operate
TOKEN = ""

MAIN_MENU_STATE, MEDIA_MENU_STATE, PRESENTATION_MENU_STATE = map(str, range(3))

MAIN_MENU_TEXT = f"{'main menu':56}."
MEDIA_MENU_TEXT = f"{'media menu':56}."

# Only admins have access to some (which currently all (which is currently one)) activities offered.
ADMINS = []