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
waiting_for_pass = False
logged_in_users = []

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    message = msg['text']
    global waiting_for_pass, password, logged_in_users

    if chat_id in logged_in_users:
        
        if '/' in message:
            command = message.replace('/', '')
        else:
            command = message
        output = os.popen('docker exec '+ container +' rcon-cli '+ command).read()
        bot.sendMessage(chat_id, output)

    if waiting_for_pass:
        if message == password:
            logged_in_users.append(chat_id)
            bot.sendMessage(chat_id, 'Success. You can control your bot now!')
            waiting_for_pass = False
        else:
            bot.sendMessage(chat_id, 'Wrong password. Try again!')

    if message == '/start' and chat_id not in logged_in_users:
        bot.sendMessage(chat_id, 'Please enter your password:')
        waiting_for_pass = True

bot = telepot.Bot(token)
MessageLoop(bot, handle).run_as_thread()

while True:
    time.sleep(5)