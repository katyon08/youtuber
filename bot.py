import telebot
import config
import youtube_downloader
import os
import logging
import time
bot = telebot.TeleBot(config.token)
print(bot.get_me())


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'кидай линку, пидр')



@bot.message_handler(content_types=['text'])
def get_link(message):
    link = message.text
    title = youtube_downloader.try_download(link, message.chat.id)
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if title in file:
                bot.send_document(message.chat.id, open(file, 'rb'))
                bot.send_audio(message.chat.id, open(file, 'rb'))
                bot.send_voice(message.chat.id, open(file, 'rb'))


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except Exception as err:
        logging.error(err)
        time.sleep(5)
        print("Internet error!")
