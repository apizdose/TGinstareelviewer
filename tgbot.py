import telebot
import os
import random
import time
import yt_dlp
import re


def tokenTGget():
    with open('token.txt','r') as tokenfile:
        return tokenfile.read()

if os.name == 'nt':
    folderpath='.\\'
else:
    folderpath='./'

TOKENTG = tokenTGget().rstrip()
bot = telebot.TeleBot(TOKENTG)

def download_with_ytdlp(reel_url):
    ydl_opts = {
        'outtmpl': 'reel.mp4', # Имя выходного файла
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([reel_url])

def get_link(text):
    patternlink = r"https?://[^\s<>\"']+|www\.[^\s<>\"']+"
    matchlink = re.search(patternlink, text)
    if matchlink:
        return matchlink.group(0)
    else:
        return None

def get_reel_id(url):
    pattern = r"/reel/([A-Za-z0-9_-]+)"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None

@bot.message_handler(content_types=['text'])
@bot.edited_message_handler(content_types=['text'])

def send_echo(message):
    if os.path.exists('reel.mp4'):
        os.remove('reel.mp4')
    if 'https://www.instagram.com/reel/' in message.text:
        reel_url = get_link(message.text)
        reel_id = get_reel_id(reel_url)
        sent_msg=bot.send_message(message.chat.id,'Начинаю скачивать рил... Пожалуйста, подожди немного.')
        download_with_ytdlp(f"https://www.instagram.com/reel/{reel_id}")
        bot.delete_message(chat_id=message.chat.id, message_id=sent_msg.message_id)
        try:
            if os.path.exists('reel.mp4'):
                with open('reel.mp4', 'rb') as video:
                    #pass
                    bot.send_video(message.chat.id, video)
        except Exception as e:
            bot.send_message(message.chat.id,'Что-то пошло не так, возможно закрытый аккаунт или удалённый рил. Попробуй ещё раз.')
    else:
        bot.send_message(message.chat.id,'Давай уже сюда ссылочку свою!')
    if os.path.exists('reel.mp4'):
        os.remove('reel.mp4')

print('\n------------------ Running...------------------')

bot.infinity_polling()
