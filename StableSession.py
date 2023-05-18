import random
import string
import json
import sys
import getpass

password = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(20))

! wget -q -c -nc https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
! tar -xvzf ngrok-v3-stable-linux-amd64.tgz
! apt-get install -qq -o=Dpkg::Use-Pty=0 openssh-server pwgen > /dev/null
! echo root:$password | chpasswd
! mkdir -p /var/run/sshd
! echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
! echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config
! echo "LD_LIBRARY_PATH=/usr/lib64-nvidia" >> /root/.bashrc
! echo "export LD_LIBRARY_PATH" >> /root/.bashrc
get_ipython().system_raw('/usr/sbin/sshd -D &')

print("Copy authtoken from https://dashboard.ngrok.com/auth")
authtoken = getpass.getpass()

get_ipython().system_raw('chmod +x ngrok && ./ngrok config add-authtoken $authtoken && ./ngrok tcp 22 &')
print("Root password: {}".format(password))

! curl -s http://localhost:4040/api/tunnels > tunnels.json

try:
    with open('tunnels.json') as file:
        json_data = file.read()
        if json_data.strip() == "":
            print("tunnels.json is empty.")
        else:
            data = json.loads(json_data)
            tunnels = data['tunnels']
            if tunnels:
                public_url = tunnels[0]['public_url']
                print("Public URL: {}".format(public_url))
            else:
                print("No tunnels available.")
except (IOError, ValueError, KeyError) as e:
    print("Error occurred while processing tunnel data:", str(e))
