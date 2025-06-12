from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.enums.parse_mode import ParseMode

from Red0xBot.bot import Red0xBot
from Red0xBot.config import Telegram
from Red0xBot.utils.translation import BUTTON

#---------- Scenes ----------#

SCENES = {
    "MAIN_MENU": 0,
    "WAITING_FOR_BOOK": 1,
    "WAITING_FOR_PAPER": 2,
    "ABOUT_ME": 3,
    "SEND_DM": 4
}

COMMANDS = [
    "Donate a book",
    "Donate a paper",
    "About me",
    "Send dm",
    "Back"
]

user_states = {}

#---------- Start ----------#

@Red0xBot.on_message(filters.command("start") & filters.private)
async def start(bot: Client, message: Message):
    user_id = message.from_user.id
    #Add db!
    if user_states.get(user_id) is None:
        await bot.send_message(
            chat_id=Telegram.OWNER_ID,
            text=f"New user started bot : \n\nName: {message.from_user.first_name}\nusername: @{message.from_user.username}\nData center: {message.from_user.dc_id}\nChatId: {message.from_user.id}",
            disable_web_page_preview=True
        )
    user_states[user_id] = SCENES["MAIN_MENU"]
    return await message.reply_text(
        text="Wellcome. What action would you take?",
        parse_mode=ParseMode.MARKDOWN,
        quote=True,
        reply_markup=BUTTON.START_BUTTONS,
        disable_web_page_preview=True
    )


#---------- scene switcher ----------#

def text_scene_filter(_, __, message: Message):
    if message.text not in COMMANDS:
        return False
    return True

text_scene = filters.create(text_scene_filter)

@Red0xBot.on_message((filters.text) & filters.private & text_scene)
async def handle_scene_switch(bot: Client, message: Message):
    user_id = message.from_user.id
    #---------- Back ----------#
    if message.text == "Back":
        user_states[user_id] = SCENES["MAIN_MENU"]
        return await message.reply_text(
            text="Ok we are in main menu",
            parse_mode=ParseMode.MARKDOWN,
            quote=True,
            reply_markup=BUTTON.START_BUTTONS,
        disable_web_page_preview=True
        )
    #---------- book scene ----------#
    if message.text == "Donate a book":
        user_states[user_id] = SCENES["WAITING_FOR_BOOK"]
        return await message.reply_text(
            text="Ok now send your book.",
            parse_mode=ParseMode.MARKDOWN,
            quote=True,
            reply_markup=BUTTON.BACK_BUTTONS,
            disable_web_page_preview=True
        )
    #---------- Paper scene ----------#
    if message.text == "Donate a paper":
        user_states[user_id] = SCENES["WAITING_FOR_PAPER"]
        return await message.reply_text(
            text="Ok now send your paper.",
            parse_mode=ParseMode.MARKDOWN,
            quote=True,
            reply_markup=BUTTON.BACK_BUTTONS,
            disable_web_page_preview=True
        )
    #---------- Send dm scene ----------#
    if message.text == "Send dm":
        user_states[user_id] = SCENES["SEND_DM"]
        return await message.reply_text(
            text="Ok now send your message.",
            parse_mode=ParseMode.MARKDOWN,
            quote=True,
            reply_markup=BUTTON.BACK_BUTTONS,
            disable_web_page_preview=True
        )
    #---------- about me ----------#
    if message.text == "About me":
        user_states[user_id] = SCENES["ABOUT_ME"]
        return await message.reply_text(
            text="my id: @maziyar_red0x",
            parse_mode=ParseMode.MARKDOWN,
            quote=True,
            reply_markup=BUTTON.BACK_BUTTONS,
            disable_web_page_preview=True
        )
    return await message.reply_text(
        text="Unkown command",
        parse_mode=ParseMode.MARKDOWN,
        quote=True,
        disable_web_page_preview=True
    )

#---------- dm function ----------#

def dm_scene_filter(_, __, message: Message):
    user_id = message.from_user.id
    if user_states.get(user_id) != SCENES["SEND_DM"]:
        return False
    return True

dm_scene = filters.create(dm_scene_filter)

@Red0xBot.on_message((filters.text) & filters.private & dm_scene)
async def sendDm(bot: Client, message: Message):
    user_id = message.from_user.id
    user_states[user_id] = SCENES["MAIN_MENU"]
    message_id = await bot.forward_messages(chat_id=Telegram.OWNER_ID, from_chat_id=message.chat.id, message_ids=message.id)
    await bot.send_message(
        chat_id=Telegram.OWNER_ID,
        text=f"New message recived From: \n\nName: {message.from_user.first_name}\nusername: @{message.from_user.username}\nData center: {message.from_user.dc_id}\nChatId: {message.from_user.id}",
        reply_to_message_id=message_id.id, # type: ignore
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Reply", callback_data=f"senddm_{message.id}_{message.from_user.id}"), # type: ignore
                    InlineKeyboardButton("Ignore", callback_data=f"senddmcancel_{message.id}_{message.from_user.id}") # type: ignore
                ]
            ]
        ),
        disable_web_page_preview=True
    )
    return await message.reply_text(
        text="✅ message has been sent to admin.",
        quote=True,
        reply_markup=BUTTON.START_BUTTONS,
        disable_web_page_preview=True
    )

#---------- paper function ----------#

def paper_scene_filter(_, __, message: Message):
    user_id = message.from_user.id
    if user_states.get(user_id) != SCENES["WAITING_FOR_PAPER"]:
        return False
    return True

paper_scene = filters.create(paper_scene_filter)

@Red0xBot.on_message((filters.document) & filters.private & paper_scene)
async def donatePaper(bot: Client, message: Message):
    user_id = message.from_user.id
    user_states[user_id] = SCENES["MAIN_MENU"]
    message_id = await bot.forward_messages(chat_id=Telegram.OWNER_ID, from_chat_id=message.chat.id, message_ids=message.id)
    await bot.send_message(
        chat_id=Telegram.OWNER_ID,
        text=f"New paper recived From: \n\nName: {message.from_user.first_name}\nusername: @{message.from_user.username}\nData center: {message.from_user.dc_id}\nChatId: {message.from_user.id}\n\nSend it to the channel?",
        reply_to_message_id=message_id.id, # type: ignore
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("YES", callback_data=f"sendpaper_{message_id.id}_{message.from_user.id}"), # type: ignore
                    InlineKeyboardButton("NO", callback_data=f"sendpapercancel_{message_id.id}_{message.from_user.id}") # type: ignore
                ]
            ]
        ),
        disable_web_page_preview=True
    )
    return await message.reply_text(
        text="✅ Paper received! Admin will review it soon.",
        quote=True,
        reply_markup=BUTTON.START_BUTTONS,
        disable_web_page_preview=True
    )

#---------- book function ----------#

def book_scene_filter(_, __, message: Message):
    user_id = message.from_user.id
    if user_states.get(user_id) != SCENES["WAITING_FOR_BOOK"]:
        return False
    return True

book_scene = filters.create(book_scene_filter)

@Red0xBot.on_message((filters.document) & filters.private & book_scene)
async def donateBook(bot: Client, message: Message):
    user_id = message.from_user.id
    user_states[user_id] = SCENES["MAIN_MENU"]
    message_id = await bot.forward_messages(chat_id=Telegram.OWNER_ID, from_chat_id=message.chat.id, message_ids=message.id)
    await bot.send_message(
        chat_id=Telegram.OWNER_ID,
        text=f"New book recived From: \n\nName: {message.from_user.first_name}\nusername: {message.from_user.username}\nData center: {message.from_user.dc_id}\nChatId: {message.from_user.id}\n\nSend it to the channel?",
        reply_to_message_id=message_id.id, # type: ignore
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("YES", callback_data=f"sendbook_{message_id.id}_{message.from_user.id}"), # type: ignore
                    InlineKeyboardButton("NO", callback_data=f"sendbookcancel_{message_id.id}_{message.from_user.id}") # type: ignore
                ]
            ]
        ),
        disable_web_page_preview=True
    )
    return await message.reply_text(
        "✅ Book received! Admin will review it soon.",
        quote=True,
        reply_markup=BUTTON.START_BUTTONS,
        disable_web_page_preview=True
    )