# crobot
telegram bot

## Hosting
the project is hosted on 
https://www.pythonanywhere.com/user/cronycles/

## Project Requirements
yo need to have **pip** installed on your system before running this project. See how to install it:
### OSX 
- if you do not have __pip__ installed please install it using the following commands on the terminal:

    - ```curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py```
    - ```python3 get-pip.py```

## Setup
- Go into project folder

- then install the requirements:

    ```pip3 install --user -r ./requirements.txt```

###pythonanywhere
```pip install --user -r ./requirements.txt```

## To launch bot 
###OSX
open terminal and launch this command
```python3 bot.py```

###pythonanywhere
```python bot.py```

## TELEGRAM BOT COMMANDS
To see if your bot works, just type on your browser:
https://api.telegram.org/bot\<bot-token>\/getMe

just open chrome and go to :
https://api.telegram.org/bot\<bot-token\>/getUpdates