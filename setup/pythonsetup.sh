#!/bin/bash
cd ${ROOT_DIR}
sudo pip3 install virtualenv
virtualenv -p /usr/bin/python3 team1
cd team1
source bin/activate
pip3 install -r requirements.txt
