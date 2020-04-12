#!/usr/bin/env python3
# ./bot.py <minecraft_container_name>

import telepot, time, os, sys
from telepot.loop import MessageLoop

container = sys.argv[1]
print('Connected to '+ container +'.')
token = os.environ['TG_TOKEN']
password = os.environ['TG_PASS']
loggedIn = False
waiting_for_pass = False

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    message = msg['text']
    global waiting_for_pass, password, loggedIn

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
    
    if loggedIn:
        if message == '/list':
            output = os.popen('docker exec '+ container +' rcon-cli list').read()
            bot.sendMessage(chat_id, output)
        
        if message == '/weather clear':
            output = os.popen('docker exec '+ container +' rcon-cli weather clear').read()
            bot.sendMessage(chat_id, output)
        if message == '/weather rain':
            output = os.popen('docker exec '+ container +' rcon-cli weather rain').read()
            bot.sendMessage(chat_id, output)
        if message == '/weather thunder':
            output = os.popen('docker exec '+ container +' rcon-cli weather thunder').read()
            bot.sendMessage(chat_id, output)

bot = telepot.Bot(token)
MessageLoop(bot, handle).run_as_thread()

while True:
    time.sleep(5)