#!/bin/sh 
# cron.sh 
# navigate to home directory, then to this directory, then execute python script, then back home  

cd /home/pi/workspace/crobot
sudo python crobot.py 

cd /
