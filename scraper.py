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

'''already use config.data
TOKEN = os.getenv('TOKEN')
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone = os.getenv('PHONE_NUMBER')
client = TelegramClient(phone, api_id, api_hash)
'''

def banner():
    print(f'''
[/!\] Baudelaire scraper [/!\]  ''')


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
    print("[!] run python setup.py -h first !!\n")
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
#chunk_size représente le nombre de messages à récupérer (max 30) sinon compte ban /!\
chunk_size = 30
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