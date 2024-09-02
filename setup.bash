#!/bin/bash

sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation utility
sudo mysql UPDATE mysql.user SET authentication_string = PASSWORD('siemsiem') WHERE User = 'root';
sudo mysql FLUSH PRIVILEGES;
sudo apt install python3
sudo apt install python3-pip
sudo apt install python3-venv
sudo python3 -m venv 050guessr_server/venv
source venv/bin/activate
sudo pip install -r 050guessr_server/requirements.txt
sudo nano 050guessr_server/keys_.py
python3 050guessr_server/setup.py
