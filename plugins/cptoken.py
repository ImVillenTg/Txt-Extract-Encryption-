import requests 
from pyrogram.types.messages_and_media import message
from pyromod import listen
from pyrogram.types import Message
import pyrogram
import asyncio
from pyrogram.types import User, Message
from pyrogram import Client, filters
from pyrogram import Client as bot
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import FloodWait
from pyrogram.types import User, Message
import main
import config
import os

ADMINS = config.ADMINS
sudo_group = config.GROUPS

@bot.on_message(filters.command("token") & (filters.chat(sudo_group) | filters.user(ADMINS)))
async def account_login(bot: Client, m: Message):
    editable = await bot.send_message(m.chat.id, f"Hello [{m.from_user.first_name}](tg://user?id={m.from_user.id}) Bruh.\nSend Classplus url txt File")
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)

    path = f"./downloads/{m.chat.id}"

    mm = ""
    if input.document.file_name:
        mm = input.document.file_name.replace(".txt", "")

    try:    
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split(":", 1))
        os.remove(x)
    except:
        await m.reply_text("Invalid file input.")
        os.remove(x)
        return

    await editable.edit(f"**Total Links found in this Txt file are : {len(links)}**\n\n**start converting link please wait patiently 📥")

    try:
        with open(f'{mm}.txt', 'w') as f:
            pdf_links = {}
            for i in range(len(links)):
                if len(links[i]) < 2:
                    continue
                url = links[i][1]
                if url.endswith(".pdf"):
                    #pdf_links.append(url)
                    name = links[i][0].strip()
                    pdf_links[name] = url
                    continue
                name = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@","").replace("*","").replace(".","").strip()

                if "classplus" in url:
                    headers = {'x-access-token': 'eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MzgzNjkyMTIsIm9yZ0lkIjoyNjA1LCJ0eXBlIjoxLCJtb2JpbGUiOiI5MTcwODI3NzQyODkiLCJuYW1lIjoiQWNlIiwiZW1haWwiOm51bGwsImlzRmlyc3RMb2dpbiI6dHJ1ZSwiZGVmYXVsdExhbmd1YWdlIjpudWxsLCJjb3VudHJ5Q29kZSI6IklOIiwiaXNJbnRlcm5hdGlvbmFsIjowLCJpYXQiOjE2NDMyODE4NzcsImV4cCI6MTY0Mzg4NjY3N30.hM33P2ai6ivdzxPPfm01LAd4JWv-vnrSxGXqvCirCSpUfhhofpeqyeHPxtstXwe0', 'user-agent': 'Mobile-Android', 'api-version': '22'}
                    params = (
                    ('url', f'{url}'),
                    )
                    response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)
                    if response.status_code != 200:
                        print("Error", name)
                        continue
                    a = response.json()['url']
                    headers1 = {'User-Agent': 'ExoPlayerDemo/1.4.37.1 (Linux;Android 11) ExoPlayerLib/2.14.1','Connection': 'keep-alive'}
                    response1 = requests.get(f'{a}', headers=headers1)
                    #b = (response1.text).split("\n")[3]
                    b = response1.text
                    if "32240524" in b:
                        b = b.split("\n")[6]
                    elif "video-sd" in b:
                        b = b.split("\n")[2]
                    elif "10000" in b:
                        b = b.split("\n")[7]
                    elif "480p" in b:
                        b = b.split("\n")[5]
                    elif "stream_0" in b:
                        b = b.split("\n")[6]
                    else:
                        b = b.split("\n")[2]
                    c = (a).rsplit("/", 1)[0]
                    url = f"{c}/{b}"

                f.write(f"{name}:{url}\n")
                #if (i+1) % 50 == 0:
                    #await asyncio.sleep(1)

        if len(pdf_links) > 0:
            with open(f'{mm}_pdf.txt', 'w') as pdf_file:
                for name, link in pdf_links.items():
                    pdf_file.write(f"{name}:{link}\n")
            await bot.send_document(m.chat.id, f"{mm}_pdf.txt", caption=f"{mm} - PDF links")
            os.remove(f"{mm}_pdf.txt")

        await bot.send_document(m.chat.id, f"{mm}.txt", caption=f"{mm} - VIDEOS links")
        os.remove(f"{mm}.txt")
        await editable.edit(f"**Total Links found in this Txt file are : {len(links)}**\n\n**Links Converting completed successfully")

    except Exception as e:
        await m.reply_text(f"{e}")
        os.remove(f"{mm}.txt")  # remove the file if an exception occurs.
