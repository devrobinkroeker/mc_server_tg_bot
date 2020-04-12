#!/usr/bin/env python3
# ./bot.py <minecraft_container_name>

import telepot, time, os, sys
from telepot.loop import MessageLoop
from pprint import pprint

container = sys.argv[1]

containers = os.popen('docker ps --format {{.Names}}').read().split('\n')
if container in containers:
    print('Connected to '+ container +'.')
else:
    print('No running container found with that name.')
    sys.exit()


token = os.environ['TG_TOKEN']
password = os.environ['TG_PASS']
loggedIn = False
waiting_for_pass = False

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    message = msg['text']
    global waiting_for_pass, password, loggedIn

    if loggedIn:
        
        if '/' in message:
            command = message.replace('/', '')
        else:
            command = message
        output = os.popen('docker exec '+ container +' rcon-cli '+ command).read()
        bot.sendMessage(chat_id, output)

    if waiting_for_pass:
        if message == password:
            loggedIn = True
            bot.sendMessage(chat_id, 'Success. You can control your bot now!')
            waiting_for_pass = False
        else:
            bot.sendMessage(chat_id, 'Wrong password. Try again!')

    if message == '/start' and loggedIn == False:
        bot.sendMessage(chat_id, 'Please enter your password:')
        waiting_for_pass = True

bot = telepot.Bot(token)
MessageLoop(bot, handle).run_as_thread()

while True:
    time.sleep(5)