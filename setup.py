import os
import sys
import time


def banner():
    os.system('cls')
    print(f"[/!\] Baudelaire scraper [/!\]")
    

def requirements():
    def csv_lib():
        banner()
        print("[*] Installing csv library")
        os.system('pip install cython numpy pandas')

    banner()
    input_csv = input('do you want to merge csv files together? (y/n): ').lower()
    if input_csv == 'y':
        csv_lib()
    else:
        pass

    print("[*] Installing requirements library...")
    os.system('pip install -r requirements.txt')
    with open('config.data', 'w') as f:
        f.write('')

    banner()
    print("[*] Requirements installed.\n")


def config_setup():
	import configparser
	banner()
	cpass = configparser.RawConfigParser()
	cpass.add_section('cred')
	xid = input( "[+] enter api ID : " )
	cpass.set('cred', 'id', xid)
	xhash = input( "[+] enter hash ID : " )
	cpass.set('cred', 'hash', xhash)
	xphone = input( "[+] enter phone number : " )
	cpass.set('cred', 'phone', xphone)
	setup = open('config.data', 'w')
	cpass.write(setup)
	setup.close()
	print( "[+] setup complete !")
     

def merge_csv():
	import pandas as pd
	import sys
	banner()
	file1 = pd.read_csv(sys.argv[2])
	file2 = pd.read_csv(sys.argv[3])
	print( '[' +'+'+ ']' +' merging '+sys.argv[2]+' & '+sys.argv[3]+' ...')
	print( '[' +'+'+ ']' +' big files can take some time ... ')
	merge = file1.merge(file2, on='username')
	merge.to_csv("output.csv", index=False)
	print( '[' +'+'+ ']' +' saved file as "output.csv"\n')
    
try:
     if len(sys.argv)<2:
          raise IndexError
     
except IndexError..