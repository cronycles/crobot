import telebot
import time
from subprocess import Popen, PIPE
import os, shutil
from telebot import types
from mutagen.mp4 import MP4
import youtube_dl
import config_user as config 
import logging
import threading

logging.basicConfig(filename=config.logFilePath, filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)

bot_token = config.telegramBotCode

bot = telebot.TeleBot(token=bot_token)

def setTags(videoInfo, filename, chat_id):
    bot.send_message(chat_id, 'Setting tags to audio file...')
    tags = MP4(filename)

    tags["\xa9nam"] = videoInfo['title']
    tags["\xa9ART"] = videoInfo['uploader']
    tags["\xa9alb"] = videoInfo['uploader']

    tags.save(filename)

def removeAllFilesIntoDownload():
    for the_file in os.listdir(config.downloadDirectory):
        file_path = os.path.join(config.downloadDirectory, the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
        

def downloadYoutubeAudio(videoName, chat_id): 
    try:
        if videoName:
            options = {
                'outtmpl': config.downloadDirectory + '/%(id)s.%(ext)s',
                'format': 'm4a'
            }
            with youtube_dl.YoutubeDL(options) as ydl:
                videoInfo = ydl.extract_info(videoName, download=True)
                filename = ydl.prepare_filename(videoInfo)
                ydl.download([videoName])

            performer = videoInfo['uploader']
            title = videoInfo['title']
            duration = videoInfo['duration']
            
            setTags(videoInfo, filename, chat_id)  
            bot.send_audio(chat_id=chat_id, audio=open(filename, 'rb'), duration=duration, performer=performer, title=title, timeout=1000)
            
        else: 
            bot.send_message(chat_id, "you must send a youtube video link")
    except Exception as e:
        logging.error("Exception occurred downloading youtube audio", exc_info=True)
        bot.send_message(chat_id, "there was an error downloading the video")
    finally: 
        removeAllFilesIntoDownload()

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
        errors = response['errors']
        logging.error(errors)
    else:
        outcome = response['output']

    return outcome

def addTorrentToTransmission(url, chat_id):
    try:
        if url:
            bot.send_message(chat_id, "adding torrent...")
            command = "transmission-remote -n " + config.transmissionUsername + ":" + config.transmissionPassword + " -a " + url
            response = sendTransmissionCommand(command)
            if "success" in response:
                return True
            else: 
                return False
        else: 
            bot.send_message(chat_id, "valid torrent url")
            return False
    except Exception as e: 
        print(e)
        return False


@bot.message_handler(commands=['start'])
def send_welcome(message): 
    bot.reply_to(message, 'Hi there, I am ready, send /help command if you want to know what I can do')

@bot.message_handler(commands=['ready'])
def send_welcome(message): 
    bot.reply_to(message, 'Yeah')

@bot.message_handler(commands=['help'])
def send_welcome(message):
    msg = '- send a youtube video link to download it as mp4 \n'
    msg += '- /ready am I alive?' 
    bot.reply_to(message, msg)

@bot.message_handler(func=lambda message: message.text is not None and message.text.startswith("https://youtu"))
def podcast_video(message): 
    chat_id = message.chat.id
    if chat_id == config.cronyclesChatId:
        bot.reply_to(message,'Start downloading video...')
        videoName = message.text
        downloadYoutubeAudio(videoName, chat_id)
    else:
        bot.reply_to(message,'user not allowed')

@bot.message_handler(func=lambda message: message.text is not None and message.text.endswith(".torrent"))
def addTorrentFromUrl(message): 
    chat_id = message.chat.id
    if chat_id == config.cronyclesChatId:
        bot.reply_to(message,'Start downloading torrent...')
        response = addTorrentToTransmission(message.text,chat_id)
        if response:
            bot.send_message(chat_id,'Torrent added')
        else:
            bot.send_message(chat_id,'Error Adding Torrent')
    else:
        bot.send_message(chat_id,'user not allowed')
    


bot.polling()
