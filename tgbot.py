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
    if 'https://www.instagram.com/reel/' in message.text:
        reel_url = get_link(message.text)
        reel_id = get_reel_id(reel_url)

        download_with_ytdlp(f"https://www.instagram.com/reel/{reel_id}")



        
    bot.send_message(message.chat.id,'Давай уже сюда ссылочку свою!')
    with open('reel.mp4', 'rb') as video:
        bot.send_video(message.chat.id, video)

@bot.message_handler(content_types=['photo'])
def send_photo(message):
    file_info = bot.get_file(message.photo[len(message.photo)-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = folderpath + file_info.file_path
    with open(src, "wb") as new_file:
        new_file.write(downloaded_file)
        
    with open(src, "rb") as new_file:
            
        bot.send_photo(message.chat.id, new_file)
        
    randm=random.randint(1,9)
    if randm <=3:
        bot.send_message(message.chat.id,'фыр-фыр-фыр')


print('\n------------------ Running...------------------')

bot.polling()
'''
while True:
    try:
        bot.polling()
    except:
        input('ERROR!')
        continue
        '''