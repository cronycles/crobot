# crobot
telegram bot

## Hosting
the project is hosted on 
https://www.crointhemorning.com/

## Project Requirements
yo need to have **nodejs** installed on your system before running this project.
   
## Setup
- Go into project folder

- install the requirements:

    ```npm run restore```
- then create a file called __config.js__ with the following content:
    ```
    #code of the telegram crobot
    telegramBotCode = 'YourTelegramBotCode'

    #this bot is protected and only works with a whitelist of chat ids. Set here your ones
    chatIdsWhiteList = [123456789, 23456789]

    #temporary downloaded directory path
    downloadDirectory= "./Downloads"

    #log path
    logFilePath= "./Logs/crobot.log"
    ```
## To launch bot 

### Use VScode?
Start the bot with the Play __Run crobot__ command

### OSX
```npm run debug```

## TELEGRAM BOT COMMANDS
To see if your bot exists, just type on your browser:
https://api.telegram.org/bot\<bot-token>\/getMe

## DEPLOY BOT
* To deploy the first you need to launch the ```npm run build```
* Then compress the result folder to a zip 
* and then update it into the crobot folder on your provider url