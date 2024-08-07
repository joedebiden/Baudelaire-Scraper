from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
import os, sys
import configparser
import csv
import time
from dotenv import load_dotenv

load_dotenv()

def banner():
    os.system('cls')
    print(f'''
 _                     _      _       _ 
| |__   __ _ _   _  __| | ___| | __ _(_)_ __ ___
| '_ \ / _` | | | |/ _` |/ _ \ |/ _` | | '__/ _ \,
| |_) | (_| | |_| | (_| |  __/ | (_| | | | |  __/
|_.__/ \__,_|\__,_|\__,_|\___|_|\__,_|_|_|  \___|

 _       _
| |_ ___| | ___  __ _ _ __ __ _ _ __ ___
| __/ _ \ |/ _ \/ _` | '__/ _` | '_ ` _ \,
| ||  __/ |  __/ (_| | | | (_| | | | | | |
 \__\___|_|\___|\__, |_|  \___|_|
                |___/

 ___  ___ _ __ __ _ _ __   ___ _ __
/ __|/ __| '__/ _` | '_ \ / _ \ '__|
\__ \ (__| | | (_| | |_) |  __/ |
|___/\___|_|  \__,_| .__/ \___|_|
                   |_|
''')

cpass = configparser.RawConfigParser()
cpass.read('config.data')

try:
    api_id = cpass['cred']['id']
    api_hash = cpass['cred']['hash']
    phone = cpass['cred']['phone']
    client = TelegramClient(phone, api_id, api_hash)
except KeyError:
    os.system('cls')
    banner()
    print("[!] run python setup.py -c first !!\n")
    sys.exit(1)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    os.system('cls')
    banner()
    client.sign_in(phone, input('[+] Enter the code: '))

os.system('cls')
banner()
chats = []
last_date = None
chunk_size = 200
groups=[]

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup:
            groups.append(chat)
    except:
        continue

print('[+] Choose a group to scrape members:\n')
i=0
for g in groups:
    print(f'[{i}] -> {g.title}')
    i+=1

print('')
g_index = input('[+] Enter a Number: ')
target_group = groups[int(g_index)]

print('[+] Fetching Members...')
time.sleep(1)

all_participants = []
offset = 0
limit = 100

while True:
    participants = client(GetParticipantsRequest(
        target_group,
        ChannelParticipantsSearch(''),
        offset,
        limit,
        hash=0
    ))
    if not participants.users:
        break
    all_participants.extend(participants.users)
    offset += len(participants.users)
    time.sleep(1)  # pour éviter les erreurs de flood

print('[+] Saving In file...')
time.sleep(1)
with open("members.csv", "w", encoding='UTF-8') as f:
    writer = csv.writer(f, delimiter=",", lineterminator="\n")
    writer.writerow(['username', 'user id', 'access hash', 'name', 'group', 'group id'])
    for user in all_participants:
        username = user.username if user.username else ""
        first_name = user.first_name if user.first_name else ""
        last_name = user.last_name if user.last_name else ""
        name = (first_name + ' ' + last_name).strip()
        writer.writerow([username, user.id, user.access_hash, name, target_group.title, target_group.id])

print('[+] Members scraped successfully.\n')
print('[+] Please wait 5 or 10 minutes before scraping another group.')
