# crobot
telegram bot

## Setup
- ```sudo apt-get install python-pip```

- Then copy __config.py__ and create a new file called __config_user.py__
- Then set the variables of the __config_user.py__. Never touch the original __config.py__


## To install dependencies
```sudo pip install -r /path/to/libraries.txt```

## To launch bot
```python crobot.py```

This initiates the server for a telegram chatbot.

##Launch boot every Raspberry Reboot

- ```sudo crontab -e```
- add the following line:
  
  ```@reboot sh /home/pi/workspace/crobot/crobot_cron.sh > /var/log/crobot.log 2>&1 &```
- save and exit
- ```sudo vi /var/log/crobot.log```
- hit a space, save and exit
- ```sudo chmod 777 /var/log/crobot.log```  
