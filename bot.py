# coding=utf-8
import os
import requests
import datetime

# import telegram
from pytube import YouTube, Playlist
from pytube.exceptions import RegexMatchError
import logging
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from time import sleep

token = "594228131:AAFwrdh7Z93jaqHcCBDahNCjE2kmla7_t3Q"
bot = telegram.Bot(token=token)


class BotHandler:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def send_audio(self, chat_id, audiofile):
        return bot.send_audio(chat_id, audio=open(audiofile, 'rb'))
        # params = {'chat_id': chat_id, 'text': text}
        # method = 'sendMessage'
        # resp = requests.post(self.api_url + method, params)
        # return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update


greet_bot = BotHandler(token)
greetings = ('здравствуй', 'привет', 'ку', 'здорово')
now = datetime.datetime.now()


def main():
    new_offset = None
    today = now.day
    hour = now.hour

    while True:
        greet_bot.get_updates(new_offset)
        last_update = greet_bot.get_last_update()
        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']

        greet_bot.send_message(last_chat_id, last_update)

        link = "https://www.youtube.com/watch?v=rfOY8ePOs_0"
        greet_bot.send_message(last_chat_id, "processing " + link)

        yt = YouTube(link)

        greet_bot.send_message(last_chat_id, "downloading " + yt.title)

        yt.streams.filter(only_audio=True, subtype='mp4').order_by('resolution').first().download(os.getcwd())

        greet_bot.send_message(last_chat_id, "downloaded " + os.path.join(os.getcwd(), yt.title))

        bot.send_audio(last_chat_id, audio=open(os.path.join(os.getcwd(), yt.title + ".mp4")))



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()