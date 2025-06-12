from Red0xBot.config import Telegram
from pyrogram import Client

if Telegram.SECONDARY:
    plugins = None
    no_updates = True
else:    
    plugins = {"root": "Red0xBot/bot/plugins"}
    no_updates=None

Red0xBot = Client(
    name = "Red0xBot",
    api_id = Telegram.API_ID,
    api_hash = Telegram.API_HASH,
    #workdir = "Red0xBot/tmp",
    in_memory=True,
    plugins = plugins,
    bot_token = Telegram.BOT_TOKEN,
    sleep_threshold = Telegram.SLEEP_THRESHOLD,
    workers = Telegram.WORKERS,
    no_updates = no_updates
)

multi_clients = {}
work_loads = {}