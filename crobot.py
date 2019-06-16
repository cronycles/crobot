from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import os
import youtube_dl
from subprocess import Popen, PIPE
from mutagen.mp4 import MP4
import config_user as config 
import logging

logging.basicConfig(filename='/var/log/crobot.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)
logging.warning('This will get logged to a file')

def setTags(videoInfo, filename):
    sendMessage('Setting tags to audio file...')
    print('setting tags to filename: %s' % filename)
    tags = MP4(filename)

    tags["\xa9nam"] = videoInfo['title']
    tags["\xa9ART"] = videoInfo['uploader']
    tags["\xa9alb"] = videoInfo['uploader']

    tags.save(filename)

def sendMessage(msg):
    if msg:
        theBot.send_message(chat_id=chat_id, text=msg)

def downloadYoutubeAudio(videoName): 
    try:
        if videoName:
            ydl_opts = {
                'outtmpl': config.downloadDirectory + '/%(uploader)s_%(upload_date)s_%(id)s.%(ext)s',
                'format': 'm4a'
            }
            ydl = youtube_dl.YoutubeDL(ydl_opts)
            with ydl:
                videoInfo = ydl.extract_info(videoName, download=True)
                filename = ydl.prepare_filename(videoInfo)
            setTags(videoInfo, filename)
            performer = videoInfo['uploader']
            title = videoInfo['title']
            duration = videoInfo['duration']
            theBot.send_audio(chat_id=chat_id, audio=open(filename, 'rb'), duration=duration, performer=performer, title=title, timeout=1000)
            os.remove(filename)
            print("file removed")
        else: 
            sendMessage('you must send "/youpodcast videolink" to download something')
    except Exception as e:
        logging.error("Exception occurred downloading youtube audio", exc_info=True)

def system_call_with_response(command):
    p = Popen(command, stderr=PIPE, stdout=PIPE, shell=True)
    output, errors = p.communicate()
    outcome = dict();  
    outcome['output'] = output
    outcome['errors'] = errors
    return outcome
    

def sendTransmissionCommand(command): 
    outcome = None
    response = system_call_with_response(command)

    if response['errors']:
        logging.error('transmission command error: ' + response['errors'])
    else:
        outcome = response['output']

    return outcome

def addTorrentToTransmission(url):
    try:
        if url:
            print('adding torrent...')
            sendMessage('Adding torrent...')
            command = "transmission-remote -n " + config.transmissionUsername + ":" + config.transmissionPassword + " -a " + url
            response = sendTransmissionCommand(command)
            if "success" in response:
                return True
            else: 
                return False
        else: 
            sendMessage('you must send "/youpodcast videolink" to download something')
            return False
    except Exception as e: 
        print(e)
        return False

def extract_arg(arg):
    try:
        splitted = arg.split()
        return splitted[1]
    except:
        return ""

def youpodcast(bot, update):
    global chat_id
    global theBot
    theBot = bot
    chat_id = update.message.chat_id

    if chat_id == config.cronyclesChatId:
        sendMessage('Start downloading video...')
        messageText = update.message.text
        videoName = extract_arg(messageText)
        downloadYoutubeAudio(videoName)
    else:
        sendMessage('user not allowed')

def addtorrent(bot, update):
    global chat_id
    global theBot
    theBot = bot
    chat_id = update.message.chat_id

    if chat_id == config.cronyclesChatId:
        messageText = update.message.text
        torrentUrl = extract_arg(messageText)
        response = addTorrentToTransmission(torrentUrl)
        if response:
            sendMessage("Torrent added")
        else:
            logging.error("Error adding torrent")
            sendMessage(response)
    else:
        sendMessage('user not allowed')



def ready(bot, update):
    global chat_id
    global theBot
    theBot = bot
    chat_id = update.message.chat_id

    sendMessage('yeah')

def start(bot, update):
    global chat_id
    global theBot
    theBot = bot
    chat_id = update.message.chat_id

    sendMessage('Hi there, I am ready, send /help command if you want to know what I can do')

def help(bot, update):
    global chat_id
    global theBot
    theBot = bot
    chat_id = update.message.chat_id

    msg = '- /youpodcast followed by a youtube video link will downloads an audio podcas for you \n'
    msg += '- /addtorrent followed by a torrent will add a torrent to transmission' 
    sendMessage(msg)

def main():
    logging.info('I am listening...')
    updater = Updater(config.telegramBotCode)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('help',help))
    dp.add_handler(CommandHandler('youpodcast',youpodcast))
    dp.add_handler(CommandHandler('ready',ready))
    dp.add_handler(CommandHandler('addtorrent',addtorrent))
    updater.start_polling()
    updater.idle()

theBot = ""
chat_id = ""
if __name__ == '__main__':
    main()
