import json
from pyrogram.types import InputMediaDocument
import subprocess
from pyrogram.types.messages_and_media import message
from pyromod import listen
from pyrogram.types import Message
import pyrogram
from pyrogram import Client, filters
from pyrogram import Client as bot
from pyrogram.types.messages_and_media import message
from pyrogram.errors import FloodWait
from pyrogram.types import User, Message
import logging
import main
import config
import os
import cloudscraper

my_data = -1001938939742
sudo_group = config.GROUPS
ADMINS = config.ADMINS

@bot.on_message(filters.command("Type2"))
async def start(bot, m):
    editable = await bot.send_message(m.chat.id, "Send **API** For Getting All Batch Available in Non Folder Application 🚀")
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
    resp = scraper.get(f'https://{raw_text05}/get/folder_courses?start=-1&parent_id=-1', headers=hdr).json()["data"]
    for data in resp:
        batch_id, batch_name, batch_price, batch_logo = (data["id"]), (data["course_name"]), (data["price"]), (data["course_thumbnail"])
        unique_set.add(batch_id)
        html1.append({"id": batch_id, "course_name": batch_name, "price": batch_price, "course_thumbnail": batch_logo})
    for category in categories:
      resp = scraper.get(f'https://{raw_text05}/get/folder_courses?exam_name={category["exam_category"]}&start=-1&parent_id=-1', headers=hdr).json()["data"]
      for data in resp:
        batch_id, batch_name, batch_price, batch_logo = (data["id"]), (data["course_name"]), (data["price"]), (data["course_thumbnail"])
        if batch_id not in unique_set:
          unique_set.add(batch_id)
          html1.append({"id": batch_id, "course_name": batch_name, "price": batch_price, "course_thumbnail": batch_logo})
            
    topicid = html1
    
    for data in topicid:
        bb = f" `{data['id']}` » {data['course_name']} ✳️ ₹{data['price']} `{data['course_thumbnail']}`\n"
        mm = raw_text05.replace("api.classx.co.in", "").replace("api.teachx.co.in", "").replace("api.appx.co.in", "").replace("api.teachx.in", "").upper()
        with open(f'{mm}.txt', 'a') as f:
            f.write(f"{bb}\n")
                 	
    caption_details = raw_text05.replace("api.classx.co.in", "").replace("api.teachx.co.in", "").replace("api.appx.co.in", "").replace("apinew.teachx.in", "").replace ("api.akamai.net.in", "").replace("api.teachx.in", "").replace("cloudflare.net.in", "").upper()
    file2 = InputMediaDocument(f"{mm}.txt", caption=f"**Title :** {caption_details} **Batch List**\n❄️ Date :** {time}")
    await bot.send_media_group(m.chat.id, [file2])
    await bot.send_media_group(my_data, [file2])
    os.remove(f"{mm}.txt")
    await bot.send_message(m.chat.id, "Grabbing Done")
       
