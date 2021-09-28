# -*- coding: utf-8 -*-

"""
Simple Telegram bot for interacting with the computer remotely from a mobile device.

Usage:
Send /start to initiate conversation or return to the main menu.
Use inline keyboards to navigate through menus and interact with them.
"""

import json
from typing import Union

from telegram import Update
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.ext import CallbackQueryHandler, ConversationHandler
import pyautogui

from config import ADMINS, MAIN_MENU_STATE, MAIN_MENU_TEXT, MEDIA_MENU_TEXT, MEDIA_MENU_STATE, TOKEN


MAIN_MENU_KEYBOARD_MARKUP = json.dumps({'inline_keyboard': [
    [{'text': 'Media', 'callback_data': MEDIA_MENU_STATE}],
]})


MEDIA_MENU_KEYBOARD_MARKUP = json.dumps({'inline_keyboard': [
    [{'text': '-5s', 'callback_data': '-5s'}, {'text': '⏯️', 'callback_data': 'play'}, {'text': '+5s', 'callback_data': '+5s'}],
    [{'text': '🔈', 'callback_data': 'vol0'}, {'text': '🔉', 'callback_data': 'vol-'}, {'text': '🔊', 'callback_data': 'vol+'}],
    [{'text': '❌', 'callback_data': 'close'}, {'text': '⏮️', 'callback_data': 'prev'}, {'text': '⏭', 'callback_data': 'next'}]
]})


def start_handler(update: Update, context: CallbackContext) -> MAIN_MENU_STATE:
    update.message.reply_text(
        MAIN_MENU_TEXT,
        reply_markup=MAIN_MENU_KEYBOARD_MARKUP
    )
    return MAIN_MENU_STATE


def main_menu_callback_handler(update: Update, context: CallbackContext) \
    -> Union[MAIN_MENU_STATE, MEDIA_MENU_STATE]:

    query = update.callback_query
    query.answer()
    data = query.data

    if data == MEDIA_MENU_STATE:
        if update.effective_chat.id in ADMINS:
            return media_menu_callback_handler(update, context)
        else:
            query.edit_message_text(
                MAIN_MENU_TEXT + "\nYou have got no permission, please contact <a href='https://t.me/true_real_michael'>the Admin</a>",
                reply_markup=MAIN_MENU_KEYBOARD_MARKUP,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
            )
            return MAIN_MENU_STATE
    else:
        query.edit_message_text(
            MAIN_MENU_TEXT,
            reply_markup=MAIN_MENU_KEYBOARD_MARKUP
        )
        return MAIN_MENU_STATE


def media_menu_callback_handler(update: Update, context: CallbackContext) \
    -> Union[MAIN_MENU_STATE, MEDIA_MENU_STATE]:

    query = update.callback_query
    query.answer()
    data = query.data

    if data == 'close':
        return main_menu_callback_handler(update, context)
    elif data == 'play': pyautogui.press('playpause')
    elif data == 'vol0': pyautogui.press('volumemute')
    elif data == 'vol-': pyautogui.press('volumedown')
    elif data == 'vol+': pyautogui.press('volumeup')
    elif data == 'prev': pyautogui.press('prevtrack')
    elif data == 'next': pyautogui.press('nexttrack')
    elif data == '-5s' : pyautogui.press('left')
    elif data == '+5s' : pyautogui.press('right')
    else:
        query.edit_message_text(
            MEDIA_MENU_TEXT,
            reply_markup=MEDIA_MENU_KEYBOARD_MARKUP
        )

    return MEDIA_MENU_STATE


def fallback_handler(update: Update, context: CallbackContext) \
    -> Union[MAIN_MENU_STATE, MEDIA_MENU_STATE]:

    update.message.reply_text("Looks like something went wrong :(\nRedirecting to the main page")
    return start_handler(update, context)


def main() -> None:
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    main_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_handler)],
        states={
            MAIN_MENU_STATE:  [CallbackQueryHandler(main_menu_callback_handler)],
            MEDIA_MENU_STATE: [CallbackQueryHandler(media_menu_callback_handler)],
        },
        fallbacks=[CallbackQueryHandler(fallback_handler)],
        allow_reentry=True,
    )

    dispatcher.add_handler(main_conversation_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
