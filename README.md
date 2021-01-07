# crobot
telegram bot

## Hosting
the project is hosted on 
https://www.pythonanywhere.com/user/cronycles/

## Project Requirements
yo need to have **pip** installed on your system before running this project. See how to install it:
### OSX 
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
   
## Setup
- Go into project folder

- install the requirements:

    ```pip3 install --user -r ./requirements.txt```
- then create a file called __config_user.py__ with the following content:
    ```
    #code of the telegram crobot
    telegramBotCode = 'YourTelegramBotCode'

    #this bot is protected and only works with one chat id. Set here your one
    myChatId = 123456789

    #temporary downloaded directory path
    downloadDirectory= "./Downloads"

    #log path
    logFilePath= "./Logs/crobot.log"
    ```
### pythonanywhere
```pip install --user -r ./requirements.txt```

## To launch bot 
###OSX
open terminal and launch this command
```python3 bot.py```

###pythonanywhere
```python bot.py```

## TELEGRAM BOT COMMANDS
To see if your bot exists, just type on your browser:
https://api.telegram.org/bot\<bot-token>\/getMe