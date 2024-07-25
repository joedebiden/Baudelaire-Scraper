from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel
from dotenv import load_dotenv
import os
import asyncio 

load_dotenv()
#go to my.telegram.org

TOKEN = os.getenv('TOKEN')
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone = os.getenv('PHONE_NUMBER')
client = TelegramClient(phone, api_id, api_hash)


# CODE ERREUR a modifier
'''Nom du canal : Remplacez 'channel_username' par le nom du canal que vous souhaitez scraper.
Nombre de messages : Modifiez le paramètre limit dans rate_limited_fetch pour définir le nombre de messages à récupérer.'''
async def rate_limited_fetch(channel_username, limit=100, requests_per_second=30):
    await client.start()
    channel = await client.get_entity(channel_username)
    
    messages = []
    offset_id = 0
    while len(messages) < limit:
        batch = await client(GetHistoryRequest(
            peer=channel,
            limit=min(100, limit - len(messages)),
            offset_id=offset_id,
            offset_date=None,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0
        ))
        
        if not batch.messages:
            break
        
        messages.extend(batch.messages)
        offset_id = batch.messages[-1].id
        
        await asyncio.sleep(1 / requests_per_second)
    
    for message in messages:
        print(message.message)

with client:
    client.loop.run_until_complete(rate_limited_fetch('channel_username', 100))