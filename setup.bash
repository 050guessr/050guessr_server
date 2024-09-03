#!/bin/bash

sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation utility
sudo mysql --user=root -e "ALTER USER 'root'@'localhost' IDENTIFIED BY 'siemsiem'; FLUSH PRIVILEGES;"
sudo apt install python3
sudo apt install python3-pip
sudo apt install python3-venv
sudo python3 -m venv 050guessr_server/venv
source 050guessr_server/venv/bin/activate
pip install -r 050guessr_server/requirements.txt 
sudo nano 050guessr_server/keys_.py
python3 050guessr_server/setup.py
