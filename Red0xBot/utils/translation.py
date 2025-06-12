from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

class BUTTON(object):
    START_BUTTONS = ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(text="Donate a book"),
                KeyboardButton(text="Donate a paper"),
                KeyboardButton(text="About me"),
            ],
            [
                KeyboardButton("Send dm")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    BACK_BUTTONS = ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("Back")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

class BUTTON_ADMIN(object):
    START_BUTTONS = ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(text="Send a book"),
                KeyboardButton(text="Send a paper"),
            ],
            [
                KeyboardButton(text="Send bulk book"),
                KeyboardButton(text="Send bulk paper"),
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    BACK_BUTTONS = ReplyKeyboardMarkup(
        [
            [
                KeyboardButton("Back")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    BULK_BOOK_BUTTONS = ReplyKeyboardMarkup(
        [
            [
                KeyboardButton(text="Back"),
                KeyboardButton(text="Send all"),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )