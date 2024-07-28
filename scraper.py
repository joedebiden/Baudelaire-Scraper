from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import os, sys
import configparser
import csv
import time
from dotenv import load_dotenv



load_dotenv()
#go to my.telegram.org for the infos

'''
already use config.data
TOKEN = os.getenv('TOKEN')
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone = os.getenv('PHONE_NUMBER')
client = TelegramClient(phone, api_id, api_hash)
'''

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
 \__\___|_|\___|\__, |_|  \__,_|_| |_| |_|
                |___/

 ___  ___ _ __ __ _ _ __   ___ _ __
/ __|/ __| '__/ _` | '_ \ / _ \ '__|
\__ \ (__| | | (_| | |_) |  __/ |
|___/\___|_|  \__,_| .__/ \___|_|
                   |_|
''')


cpass = configparser.RawConfigParser()
cpass.read('config.data')

#bien penser à avoir le fichier .data (suivre le setup.py)
try:
    api_id = cpass['cred']['id']
    api_hash = cpass['cred']['hash']
    phone = cpass['cred']['phone']
    client = TelegramClient(phone, api_id, api_hash)

#si le code ne le trouve pas
except KeyError:
    os.system('cls') #windows only /!\,
    banner()
    print("[!] run python setup.py -c first !!\n")
    sys.exit(1)

#utile pour la premier connexion, apres créé un fichier .session
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
             hash = 0
         ))
chats.extend(result.chats)

#https://docs.telethon.dev/en/stable/basic/quick-start.html
for chat in chats:
    try:
        if chat.megagroup==True:
            groups.append(chat)
    except:
        continue 

print('[+] Choose a group to scrape members:\n')
i=0
for g in groups:
    print('['+str(i)+']->' + g.title)
    i+=1

print('')
g_index=input('[+] Enter a Number: ')
target_group=groups[int(g_index)]

print('[+] Fetching Members...')
time.sleep(1)
all_participants = []
all_participants = client.get_participants(target_group, aggressive=True)

print('[+] Saving In file...')
time.sleep(1)
with open("members.csv", "w", encoding='UTF-8') as f:
    writer = csv.writer(f, delimiter=",", lineterminator="\n")
    writer.writerow(['username', 'user id', 'access hash', 'name', 'group', 'group id'])
    for user in all_participants:
        if user.username:
            username= user.username
        else:
            username= ""
        if user.first_name:
            first_name= user.first_name
        else:
            first_name= ""
        if user.last_name:
            last_name= user.last_name
        else:
            last_name= ""
        name= (first_name + ' ' + last_name).strip()
        writer.writerow([username, user.id, user.access_hash, name, target_group.title, target_group.id])
print('[+] Members scraped successfully.\n')
print('[+] Please wait 5 or 10 minutes before scraping another group.')
