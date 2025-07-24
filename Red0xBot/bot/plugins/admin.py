from time import sleep

from pyrogram import filters, Client
from pyrogram.types import Message, CallbackQuery
from pyrogram.enums.parse_mode import ParseMode
from datetime import datetime, timezone

from Red0xBot.bot import Red0xBot
from Red0xBot.config import Telegram
from Red0xBot.utils.translation import BUTTON_ADMIN
from Red0xBot.db.csv_db import add_record, mainFunc, searchFunc

SCENES = {
    "MAIN_MENU": 0,
    "PENDING_REPLY": 1,
    "PENDING_BOOK": 2,
    "PENDING_BOOK_CAPTION": 3,
    "PENDING_BOOK_TOPIC": 4,
    "PENDING_PAPER": 5,
    "PENDING_PAPER_CAPTION": 6,
    "PENDING_BULK_BOOK": 7,
    "PENDING_BULK_BOOK_CAPTION": 8,
    "PENDING_BULK_BOOK_TOPIC": 9
}

COMMANDS = [
    "Send a book",
    "Send a paper",
    "Send bulk book",
    "Send bulk paper",
    "Back"
]

MESSAGE_PROPERTIES = {
    "reply_to": 0,
    "reply_message": 0
}

user_states = {}

@Red0xBot.on_message(filters.command("start") & filters.private & filters.user(Telegram.OWNER_ID))
async def start_admin(bot: Client, message: Message):
    user_states[Telegram.OWNER_ID] = SCENES["MAIN_MENU"]
    return await message.reply_text(
        text="Wellcome. What action would you take?",
        parse_mode=ParseMode.MARKDOWN,
        quote=True,
        reply_markup=BUTTON_ADMIN.START_BUTTONS,
        disable_web_page_preview=True
    )

@Red0xBot.on_callback_query(filters.user(Telegram.OWNER_ID))
async def cb_data(bot: Client, update: CallbackQuery):
    usr_cmd: [str] = update.data.split("_") # type: ignore
    # ------------ Book ------------#
    if usr_cmd[0] == "sendbookcancel":
        return await update.message.edit_text(
            text="Ok, operation has been canceled.",
            disable_web_page_preview=True,
        )
    if usr_cmd[0] == "sendbook":
        original_message = await bot.get_messages(chat_id=int(usr_cmd[2]), message_ids=int(usr_cmd[1]))
        if not original_message.document: # type: ignore
            return await update.message.edit_text(
                text="There was an error!",
                disable_web_page_preview=True
            )
        await update.message.edit_text(
            text="Ok, book has been sent to channel",
            disable_web_page_preview=True
        )
        return await bot.send_document(
            chat_id=Telegram.BOOK_CHANNEL,
            document=original_message.document.file_id, # type: ignore
            caption="#book\n\n@Red0x_Library"
        )
    # ------------ Paper ------------#
    if usr_cmd[0] == "sendpapercancel":
        return await update.message.edit_text(
            text="Ok, operation has been canceled.",
            disable_web_page_preview=True,
        )
    if usr_cmd[0] == "sendpaper":
        original_message = await bot.get_messages(chat_id=int(usr_cmd[2]), message_ids=int(usr_cmd[1]))
        if not original_message.document: # type: ignore
            return await update.message.edit_text(
                text="There was an error!",
                disable_web_page_preview=True
            )
        await update.message.edit_text(
            text="Ok, paper has been sent to channel",
            disable_web_page_preview=True
        )
        return await bot.send_document(
            chat_id=Telegram.BOOK_CHANNEL,
            document=original_message.document.file_id, # type: ignore
            caption="#paper\n\n@Red0x_Library"
        )
    # ------------ Dm ------------#
    if usr_cmd[0] == "senddmcancel":
        return await update.message.edit_text(
            text="Ok, operation has been canceled.",
            disable_web_page_preview=True,
        )
    if usr_cmd[0] == "senddm":
        user_states[Telegram.OWNER_ID] = SCENES["PENDING_REPLY"]
        MESSAGE_PROPERTIES["reply_to"] = int(usr_cmd[2])
        MESSAGE_PROPERTIES["reply_message"] = int(usr_cmd[1])
        return await update.message.edit_text(
            text="Ok, write your reply to send.",
            disable_web_page_preview=True
        )
    return
    
#---------- scene switcher ----------#

def text_scene_filter(_, __, message: Message):
    if message.text not in COMMANDS:
        return False
    return True

text_scene = filters.create(text_scene_filter)

@Red0xBot.on_message((filters.text) & filters.private & text_scene & filters.user(Telegram.OWNER_ID))
async def handle_scene_switch(bot: Client, message: Message):
    user_id = message.from_user.id
    #---------- bulk book ----------#
    if message.text == "Send bulk book":
        user_states[Telegram.OWNER_ID] = SCENES["PENDING_BULK_BOOK"]
        return await message.reply_text(
            text="Ok send your book",
            parse_mode=ParseMode.MARKDOWN,
            quote=True,
            reply_markup=BUTTON_ADMIN.BACK_BUTTONS,
            disable_web_page_preview=True
        )
    #---------- Single book ----------#
    if message.text == "Send a book":
        user_states[Telegram.OWNER_ID] = SCENES["PENDING_BOOK"]
        return await message.reply_text(
            text="Ok send your book",
            parse_mode=ParseMode.MARKDOWN,
            quote=True,
            reply_markup=BUTTON_ADMIN.BACK_BUTTONS,
            disable_web_page_preview=True
        )
    #---------- Single book ----------#
    if message.text == "Send a paper":
        user_states[Telegram.OWNER_ID] = SCENES["PENDING_PAPER"]
        return await message.reply_text(
            text="Ok send your paper",
            parse_mode=ParseMode.MARKDOWN,
            quote=True,
            reply_markup=BUTTON_ADMIN.BACK_BUTTONS,
            disable_web_page_preview=True
        )
    #---------- Back ----------#
    if message.text == "Back":
        user_states[Telegram.OWNER_ID] = SCENES["MAIN_MENU"]
        BULK_BOOK_PROPERTIES_ARR.clear()
        i["number"] = 0
        return await message.reply_text(
            text="Ok we are in main menu",
            parse_mode=ParseMode.MARKDOWN,
            quote=True,
            reply_markup=BUTTON_ADMIN.START_BUTTONS,
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
    if user_states.get(Telegram.OWNER_ID) != SCENES["PENDING_REPLY"]:
        return False
    return True

dm_scene = filters.create(dm_scene_filter)

@Red0xBot.on_message((filters.text) & filters.private & dm_scene & filters.user(Telegram.OWNER_ID))
async def sendDm(bot: Client, message: Message):
    user_states[Telegram.OWNER_ID] = SCENES["MAIN_MENU"]
    await bot.send_message(
        chat_id=MESSAGE_PROPERTIES["reply_to"],
        text=f"Admin replied: {message.text}",
        reply_to_message_id=MESSAGE_PROPERTIES["reply_message"],
        disable_web_page_preview=True
    )
    MESSAGE_PROPERTIES["reply_to"] = 0
    MESSAGE_PROPERTIES["reply_message"] = 0
    return await message.reply_text(
        text="✅ message has been sent.",
        quote=True,
        disable_web_page_preview=True
    )

#----------------------------------------------------------------------#
#
#
#
#
#
#----------------------------------------------------------------------#

#---------- send single book function ----------#

SINGLE_BOOK_PROPERTIES: dict[str, str] = {
    "book_id": "",
    "book_caption": "",
    "book_topic": ""
}

def singleBook_scene_filter(_, __, message: Message):
    if user_states.get(Telegram.OWNER_ID) != SCENES["PENDING_BOOK"]:
        return False
    return True

singleBook_scene = filters.create(singleBook_scene_filter)

@Red0xBot.on_message((filters.document) & filters.private & singleBook_scene & filters.user(Telegram.OWNER_ID))
async def singleBook(bot: Client, message: Message):
    user_states[Telegram.OWNER_ID] = SCENES["PENDING_BOOK_TOPIC"]
    SINGLE_BOOK_PROPERTIES["book_id"] = message.document.file_id
    return await message.reply_text(
        text="Now send your topic.",
        quote=True,
        disable_web_page_preview=True,
        reply_markup=BUTTON_ADMIN.BACK_BUTTONS
    )

#---------- send single book topic function ----------#

def singleBookTopic_scene_filter(_, __, message: Message):
    if user_states.get(Telegram.OWNER_ID) != SCENES["PENDING_BOOK_TOPIC"]:
        return False
    return True

singleBookTopic_scene = filters.create(singleBookTopic_scene_filter)

@Red0xBot.on_message((filters.text) & filters.private & singleBookTopic_scene & filters.user(Telegram.OWNER_ID))
async def singleBookTopic(bot: Client, message: Message):
    user_states[Telegram.OWNER_ID] = SCENES["PENDING_BOOK_CAPTION"]
    SINGLE_BOOK_PROPERTIES["book_topic"] = message.text
    return await message.reply_text(
        text="Now send your caption.",
        quote=True,
        disable_web_page_preview=True,
        reply_markup=BUTTON_ADMIN.BACK_BUTTONS
    )

#---------- send single book caption function ----------#

def singleBookCaption_scene_filter(_, __, message: Message):
    if user_states.get(Telegram.OWNER_ID) != SCENES["PENDING_BOOK_CAPTION"]:
        return False
    return True

singleBookCaption_scene = filters.create(singleBookCaption_scene_filter)

@Red0xBot.on_message((filters.text) & filters.private & singleBookCaption_scene & filters.user(Telegram.OWNER_ID))
async def singleBookCaption(bot: Client, message: Message):
    user_states[Telegram.OWNER_ID] = SCENES["MAIN_MENU"]
    SINGLE_BOOK_PROPERTIES["book_caption"] = message.text
    isTrue = mainFunc()
    if isTrue == True:
        pass
    else:
        SINGLE_BOOK_PROPERTIES["book_id"] = ""
        SINGLE_BOOK_PROPERTIES["book_caption"] = ""
        SINGLE_BOOK_PROPERTIES["book_topic"] = ""
        return await message.reply_text(
            text="There was an error while processing your book",
            quote=True,
            disable_web_page_preview=True,
            reply_markup=BUTTON_ADMIN.START_BUTTONS
        )
    res = searchFunc(SINGLE_BOOK_PROPERTIES["book_caption"])
    if res is None:
        pass
    else:
        SINGLE_BOOK_PROPERTIES["book_id"] = ""
        SINGLE_BOOK_PROPERTIES["book_caption"] = ""
        SINGLE_BOOK_PROPERTIES["book_topic"] = ""
        user_states[Telegram.OWNER_ID] = SCENES["MAIN_MENU"]
        return await message.reply_text(
            text="Your book is exist in database\nYou may try with another book",
            quote=True,
            disable_web_page_preview=True,
            reply_markup=BUTTON_ADMIN.START_BUTTONS
        )
    add_record(
        book_name = SINGLE_BOOK_PROPERTIES["book_caption"],
        created_at = datetime.now(timezone.utc),
        author = f"{Telegram.OWNER_ID}",
        topic = SINGLE_BOOK_PROPERTIES["book_topic"],
    )
    await bot.send_document(
        chat_id=Telegram.BOOK_CHANNEL,
        document=SINGLE_BOOK_PROPERTIES.get("book_id"), # type: ignore
        caption=f"{SINGLE_BOOK_PROPERTIES.get("book_caption")}\n\n#book {SINGLE_BOOK_PROPERTIES.get("book_topic")}\n\n@Red0x_Library"
    )
    SINGLE_BOOK_PROPERTIES["book_id"] = ""
    SINGLE_BOOK_PROPERTIES["book_caption"] = ""
    SINGLE_BOOK_PROPERTIES["book_topic"] = ""
    return await message.reply_text(
        text="Your book has been sent to channel",
        quote=True,
        disable_web_page_preview=True,
        reply_markup=BUTTON_ADMIN.START_BUTTONS
    )

#----------------------------------------------------------------------#
#
#
#
#
#
#----------------------------------------------------------------------#

#---------- send single paper function ----------#

SINGLE_PAPER_PROPERTIES: dict[str, str] = {
    "paper_id": "",
    "paper_caption": ""
}

def singlePaper_scene_filter(_, __, message: Message):
    if user_states.get(Telegram.OWNER_ID) != SCENES["PENDING_PAPER"]:
        return False
    return True

singlePaper_scene = filters.create(singlePaper_scene_filter)

@Red0xBot.on_message((filters.document) & filters.private & singlePaper_scene & filters.user(Telegram.OWNER_ID))
async def singlePaper(bot: Client, message: Message):
    user_states[Telegram.OWNER_ID] = SCENES["PENDING_PAPER_CAPTION"]
    SINGLE_PAPER_PROPERTIES["paper_id"] = message.document.file_id
    return await message.reply_text(
        text="Now send your caption.",
        quote=True,
        disable_web_page_preview=True,
        reply_markup=BUTTON_ADMIN.BACK_BUTTONS
    )

#---------- send single paper caption function ----------#

def singlePaperCaption_scene_filter(_, __, message: Message):
    if user_states.get(Telegram.OWNER_ID) != SCENES["PENDING_PAPER_CAPTION"]:
        return False
    return True

singlePaperCaption_scene = filters.create(singlePaperCaption_scene_filter)

@Red0xBot.on_message((filters.text) & filters.private & singlePaperCaption_scene & filters.user(Telegram.OWNER_ID))
async def singlePaperCaption(bot: Client, message: Message):
    user_states[Telegram.OWNER_ID] = SCENES["MAIN_MENU"]
    SINGLE_PAPER_PROPERTIES["paper_caption"] = message.text
    await bot.send_document(
        chat_id=Telegram.BOOK_CHANNEL,
        document=SINGLE_PAPER_PROPERTIES.get("paper_id"), # type: ignore
        caption=f"{SINGLE_PAPER_PROPERTIES.get("paper_caption")}\n\n#paper\n\n@Red0x_Library"
    )
    SINGLE_PAPER_PROPERTIES["paper_caption"] = ""
    SINGLE_PAPER_PROPERTIES["paper_id"] = ""
    return await message.reply_text(
        text="Your paper has been sent to channel",
        quote=True,
        disable_web_page_preview=True,
        reply_markup=BUTTON_ADMIN.START_BUTTONS
    )

#----------------------------------------------------------------------#
#
#
#
#
#
#----------------------------------------------------------------------#

#---------- send bulk book function ----------#

i: dict[str, int] = {
    "number": 0
}

BULK_BOOK_PROPERTIES_ARR = []

def bulkBook_scene_filter(_, __, message: Message):
    if user_states.get(Telegram.OWNER_ID) != SCENES["PENDING_BULK_BOOK"]:
        return False
    return True

bulkBook_scene = filters.create(bulkBook_scene_filter)

@Red0xBot.on_message((filters.document) & filters.private & bulkBook_scene & filters.user(Telegram.OWNER_ID))
async def bulkBook(bot: Client, message: Message):
    user_states[Telegram.OWNER_ID] = SCENES["PENDING_BULK_BOOK_TOPIC"]
    SINGLE_BOOK_PROPERTIES["book_id"] = message.document.file_id
    return await message.reply_text(
        text="Now send your topic.",
        quote=True,
        disable_web_page_preview=True,
        reply_markup=BUTTON_ADMIN.BACK_BUTTONS
    )

#---------- send bulk book topic function ----------#

def bulkBookTopic_scene_filter(_, __, message: Message):
    if user_states.get(Telegram.OWNER_ID) != SCENES["PENDING_BULK_BOOK_TOPIC"]:
        return False
    return True

bulkBookTopic_scene = filters.create(bulkBookTopic_scene_filter)

@Red0xBot.on_message((filters.text) & filters.private & bulkBookTopic_scene & filters.user(Telegram.OWNER_ID))
async def bulkBookTopic(bot: Client, message: Message):
    user_states[Telegram.OWNER_ID] = SCENES["PENDING_BULK_BOOK_CAPTION"]
    SINGLE_BOOK_PROPERTIES["book_topic"] = message.text
    return await message.reply_text(
        text="Now send your caption.",
        quote=True,
        disable_web_page_preview=True,
        reply_markup=BUTTON_ADMIN.BACK_BUTTONS
    )

#---------- send bulk book caption function ----------#

def bulkBookCaption_scene_filter(_, __, message: Message):
    if user_states.get(Telegram.OWNER_ID) != SCENES["PENDING_BULK_BOOK_CAPTION"]:
        return False
    return True

bulkBookCaption_scene = filters.create(bulkBookCaption_scene_filter)

@Red0xBot.on_message((filters.text) & filters.private & bulkBookCaption_scene & filters.user(Telegram.OWNER_ID))
async def bulkBookCaption(bot: Client, message: Message):
    user_states[Telegram.OWNER_ID] = SCENES["PENDING_BULK_BOOK"]
    SINGLE_BOOK_PROPERTIES["book_caption"] = message.text
    res = searchFunc(SINGLE_BOOK_PROPERTIES["book_caption"])
    if res is None:
        pass
    else:
        SINGLE_BOOK_PROPERTIES["book_id"] = ""
        SINGLE_BOOK_PROPERTIES["book_caption"] = ""
        SINGLE_BOOK_PROPERTIES["book_topic"] = ""
        user_states[Telegram.OWNER_ID] = SCENES["PENDING_BULK_BOOK"]
        return await message.reply_text(
            text="Your book is exist in database\nYou may try with another book",
            quote=True,
            disable_web_page_preview=True,
            reply_markup=BUTTON_ADMIN.BULK_BOOK_BUTTONS
        )
    i["number"] = i["number"] + 1
    BULK_BOOK_PROPERTIES_ARR.insert(i["number"], SINGLE_BOOK_PROPERTIES.copy())
    SINGLE_BOOK_PROPERTIES["book_caption"] = ""
    SINGLE_BOOK_PROPERTIES["book_id"] = ""
    SINGLE_BOOK_PROPERTIES["book_topic"] = ""
    return await message.reply_text(
        text=f"Added[{i['number']}]\nSend your next book",
        quote=True,
        disable_web_page_preview=True,
        reply_markup=BUTTON_ADMIN.BULK_BOOK_BUTTONS
    )

#---------- send bulk book to channel function ----------#

def sendBulkBook_scene_filter(_, __, message: Message):
    if user_states.get(Telegram.OWNER_ID) != SCENES["PENDING_BULK_BOOK_CAPTION"] and message.text != "Send all":
        return False
    return True

sendBulkBook_scene = filters.create(sendBulkBook_scene_filter)

@Red0xBot.on_message((filters.text) & filters.private & sendBulkBook_scene & filters.user(Telegram.OWNER_ID))
async def sendBulkBook(bot: Client, message: Message):
    user_states[Telegram.OWNER_ID] = SCENES["MAIN_MENU"]
    isTrue = mainFunc()
    if isTrue == True:
        pass
    else:
        return await message.reply_text(
            text="There was an error while processing your book",
            quote=True,
            disable_web_page_preview=True,
            reply_markup=BUTTON_ADMIN.START_BUTTONS
        )
    for b in BULK_BOOK_PROPERTIES_ARR:
        add_record(
            book_name = b["book_caption"],
            created_at = datetime.now(timezone.utc),
            author = f"{Telegram.OWNER_ID}",
            topic = b["book_topic"],
        )
        await bot.send_document(
            chat_id=Telegram.BOOK_CHANNEL,
            document=b["book_id"], # type: ignore
            caption=f"{b["book_caption"]}\n\n#book {b["book_topic"]}\n\n@Red0x_Library"
        )
        sleep(0.5)
    i["number"] = 0
    BULK_BOOK_PROPERTIES_ARR.clear()
    return await message.reply_text(
        text=f"All books has been sent to your channel.",
        quote=True,
        disable_web_page_preview=True,
        reply_markup=BUTTON_ADMIN.START_BUTTONS
    )

#----------------------------------------------------------------------#
#
#
#
#
#
#----------------------------------------------------------------------#