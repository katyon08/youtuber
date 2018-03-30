import telebot
import sys
import os
import re
import sqlite3
import requests
import pytube
import config
from pytube import YouTube, Playlist
from pytube.exceptions import RegexMatchError

def try_download(link, message_id):
    try:
        yt = YouTube(link)
        if not exist(os.getcwd(), yt.title):
            try:
                yt.streams.filter(only_audio=True, subtype='mp4').order_by('resolution').first().download(os.getcwd())
            except KeyError:
                bot.send_message(message_id,u"OOPS! С этим видео что-то не так! Скинь эту ссылку на katyon08@yandex.ru, мой хазяин попытается это починить!")
            except RegexMatchError:
                bot.send_message(message_id,u"OOPS! С этим видео что-то не так! Скинь эту ссылку на katyon08@yandex.ru, мой хазяин попытается это починить!")
            except AttributeError:
                bot.send_message(message_id,u"OOPS! С этим видео что-то не так! Скинь эту ссылку на katyon08@yandex.ru, мой хазяин попытается это починить!")
            except UnicodeDecodeError:
                bot.send_message(message_id,u"OOPS! С этим видео что-то не так! Скинь эту ссылку на katyon08@yandex.ru, мой хазяин попытается это починить!")
            except TypeError:
                bot.send_message(message_id,u"OOPS! С этим видео что-то не так! Скинь эту ссылку на katyon08@yandex.ru, мой хазяин попытается это починить!")
        return yt.title.replace(',', '')
    except pytube.exceptions.RegexMatchError:
        bot.send_message(message_id, u"Я не вижу тут видео")

def exist(in_path, in_file):
    for root, dirs, files in os.walk(in_path):
        for file in files:
            if in_file in file:
                return True
    return False
