from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel

api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
phone = 'YOUR_PHONE_NUMBER'
client = TelegramClient(phone, api_id, api_hash)

async def scrape_messages(channel_username, limit=100):
    await client.start()
    channel = await client.get_entity(channel_username)
    messages = await client(GetHistoryRequest(
        peer=channel,
        limit=limit,
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0
    ))
    for message in messages.messages:
        print(message.message)

with client:
    client.loop.run_until_complete(scrape_messages('channel_username', 100))
