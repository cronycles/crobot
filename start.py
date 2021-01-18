import os
import subprocess
from threading import Thread
import crobot

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    message = 'Hello crobot!\n'
    return [message.encode()]

def start_crobot():
    crobot.start()
    
thread = Thread(target = start_crobot, args = [])
thread.start()