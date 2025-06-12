import sys
import asyncio
import logging
import traceback
import os
import logging.handlers as handlers
from aiohttp import web
from pyrogram import idle

from Red0xBot.config import Telegram, Server
from Red0xBot.bot import Red0xBot
from Red0xBot.server import web_server
from Red0xBot.bot.clients import initialize_clients

os.mkdir("Red0xBot/tmp")

logging.basicConfig(
    level=logging.INFO,
    datefmt="%d/%m/%Y %H:%M:%S",
    format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(stream=sys.stdout), handlers.RotatingFileHandler("Red0xBot/tmp/red0xbot.log", mode="a", maxBytes=104857600, backupCount=2, encoding="utf-8")]
)

logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)

server = web.AppRunner(web_server())

loop = asyncio.get_event_loop()

async def start_services():
    if Telegram.SECONDARY:
        logging.info("Starting as Secondary Server")
    else:
        logging.info("Starting as Primary Server")
    logging.info("Initializing Telegram Bot")
    await Red0xBot.start()
    bot_info = await Red0xBot.get_me()
    Red0xBot.id = bot_info.id # type: ignore
    Red0xBot.username = bot_info.username # type: ignore
    Red0xBot.fname = bot_info.first_name # type: ignore
    logging.info("Telegram bot has been initialized")
    logging.info("Initializing Clients")
    await initialize_clients() # type: ignore
    logging.info("Clients has been initialized")
    logging.info("Initializing Web Server")
    await server.setup()
    await web.TCPSite(server, Server.BIND_ADDRESS, Server.PORT).start()
    logging.info("Web Server has been initialized")
    logging.info("Service Started")
    logging.info("bot =>> {}".format(bot_info.first_name))
    if bot_info.dc_id:
        logging.info("DC ID =>> {}".format(str(bot_info.dc_id)))
    logging.info("URL =>> {}".format(Server.URL))
    await idle()

async def cleanup():
    await server.cleanup()
    await Red0xBot.stop()

if __name__ == "__main__":
    try:
        loop.run_until_complete(start_services())
    except KeyboardInterrupt:
        pass
    except Exception as err:
        logging.error(traceback.format_exc())
    finally:
        loop.run_until_complete(cleanup())
        loop.stop()
        logging.info("Stopped Services")