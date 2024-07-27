import os
import sys
import time


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
    

def requirements():
    def csv_lib():
        banner()
        print("[*] Installing csv library...")
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
	print(  '[+] merging '+sys.argv[2]+' & '+sys.argv[3]+' ...')
	merge = file1.merge(file2, on='username')
	merge.to_csv("output.csv", index=False)
	print(  '[+] saved file as "output.csv"\n')
    
    #setup code main
if len(sys.argv) > 1:
    try:
        if any([sys.argv[1] == '--config', sys.argv[1] == '-c']):
            config_setup()
        elif any([sys.argv[1] == '--merge', sys.argv[1] == '-m']):
            print('[+] merging selected')
            merge_csv()
        elif any([sys.argv[1] == '--install', sys.argv[1] == '-i']):
            requirements()
        elif any([sys.argv[1] == '--help', sys.argv[1] == '-h']):
            banner()
            print("""
to merge your files do : python setup.py -m file1.csv file2.csv

( --config  / -c ) setup api configuration
( --merge   / -m ) merge 2 .csv files in one 
( --install / -i ) install requirements
        """)    
            

        else:
            banner()
            print('\n[!] unknown argument : ' + sys.argv[1])
            print('[!] for help use : ')
            print(' python setup.py -h\n')


    except IndexError:
        banner()
        print('\n[!] need more argument on the command, like python setup.py -m file1.csv file2.csv...')
        print('[!] for help use : ')
        print(' python setup.py -h\n')


else:
    banner()
    print('\n[!] no argument given')
    print('[!] for help use : ')
    print('[!] => python setup.py -h\n')
    print('[!] and check my github page https://github.com/joedebiden/Baudelaire-Scraper')



# thanks to th3unkn0n