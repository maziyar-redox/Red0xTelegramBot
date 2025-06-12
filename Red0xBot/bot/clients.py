import asyncio
import logging
import typing
from os import environ
from pyrogram import Client

from Red0xBot.config import Telegram
from Red0xBot.bot import multi_clients, work_loads, Red0xBot


async def initialize_clients():
    all_tokens = dict(
        (c + 1, t)
        for c, (_, t) in enumerate(
            filter(
                lambda n: n[0].startswith("MULTI_TOKEN"), sorted(environ.items())
            )
        )
    )
    if not all_tokens:
        multi_clients[0] = Red0xBot
        work_loads[0] = 0
        logging.info("No additional clients found, using default client")
        return 0
    
    async def start_client(client_id, token):
        try:
            if len(token) >= 100:
                session_string = token
                bot_token = None
                logging.info(f"Starting Client - {client_id} Using Session String")
            else:
                session_string = None
                bot_token = token
                logging.info(f"Starting Client - {client_id} Using Bot Token")
            if client_id == len(all_tokens):
                await asyncio.sleep(2)
                logging.info("This will take some time, please wait...")
            client = await Client(
                name = str(client_id),
                api_id=Telegram.API_ID,
                api_hash = Telegram.API_HASH,
                bot_token = bot_token,
                sleep_threshold = Telegram.SLEEP_THRESHOLD,
                no_updates = True,
                session_string = session_string,
                in_memory = True,
            ).start()
            client.id = (await client.get_me()).id # type: ignore
            work_loads[client_id] = 0
            return client_id, client
        except Exception:
            logging.error(f"Failed starting Client - {client_id} Error:", exc_info=True)
    
    clients = await asyncio.gather(*[start_client(i, token) for i, token in all_tokens.items()])
    multi_clients.update(dict(clients)) # type: ignore
    if len(multi_clients) != 1:
        Telegram.MULTI_CLIENT = True
        logging.info("Multi-Client Mode Enabled")
        return
    else:
        logging.info("No additional clients were initialized, using default client")
        return