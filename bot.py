# coding=utf-8
import os

import pytube
import requests
import datetime

# import telegram
import sys
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
now = datetime.datetime.now()


def main():
    last = None
    try:
        while True:
            greet_bot.get_updates()
            last_update = greet_bot.get_last_update()
            last_update_id = last_update['update_id']
            last_chat_text = last_update['message']['text']
            last_chat_id = last_update['message']['chat']['id']
            last_chat_name = last_update['message']['chat']['first_name']

            if last is None or last_chat_text not in last:

                if last is None:
                    greet_bot.send_message(last_chat_id, u"Пришли мне ссылку на ютуб")
                    last = last_chat_text
                else:
                    link = last_chat_text
                    # "https://www.youtube.com/watch?v=rfOY8ePOs_0"

                    try:
                        yt = YouTube(link)

                        if not exist(os.getcwd(), yt.title):
                            try:
                                yt.streams.filter(only_audio=True, subtype='mp4').order_by('resolution').first().download(os.getcwd())
                            except KeyError:
                                greet_bot.send_message(last_chat_id,
                                                       u"OOPS! С этим видео что-то не так! Скинь эту ссылку на katyon08@yandex.ru, мой хазяин попытается это починить!")

                            except RegexMatchError:
                                greet_bot.send_message(last_chat_id,
                                                       u"OOPS! С этим видео что-то не так! Скинь эту ссылку на katyon08@yandex.ru, мой хазяин попытается это починить!")

                            except AttributeError:
                                greet_bot.send_message(last_chat_id,
                                                       u"OOPS! С этим видео что-то не так! Скинь эту ссылку на katyon08@yandex.ru, мой хазяин попытается это починить!")

                            except UnicodeDecodeError:
                                greet_bot.send_message(last_chat_id,
                                                       u"OOPS! С этим видео что-то не так! Скинь эту ссылку на katyon08@yandex.ru, мой хазяин попытается это починить!")

                            except TypeError:
                                greet_bot.send_message(last_chat_id,
                                                       u"OOPS! С этим видео что-то не так! Скинь эту ссылку на katyon08@yandex.ru, мой хазяин попытается это починить!")

                        for root, dirs, files in os.walk(os.getcwd()):
                            for file in files:
                                if yt.title in file:
                                    try:
                                        bot.send_document(last_chat_id, document=open(file, 'rb'))
                                        bot.send_audio(last_chat_id, audio=open(file, 'rb'))
                                        bot.send_voice(last_chat_id, voice=open(file, 'rb'))
                                    except telegram.error.TimedOut:
                                        pass
                    except pytube.exceptions.RegexMatchError:
                        greet_bot.send_message(last_chat_id,
                                               u"Я не вижу тут видео")

                    last = None
    except StandardError:
        pass



def exist(in_path, in_file):
    for root, dirs, files in os.walk(in_path):
        for file in files:
            if in_file in file:
                return True
    return False



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()