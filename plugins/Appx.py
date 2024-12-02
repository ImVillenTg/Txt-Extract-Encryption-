# Updated Appx.py with Messages

import json
import requests
from pyrogram.types import InputMediaDocument
from pyrogram import Client, filters
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import time
import os
import cloudscraper
import datetime

# Configurations
time = datetime.datetime.now().strftime("%d-%m-%Y")
my_data = -1001938939742  # Example Group ID
sudo_group = []  # Your sudo group here
ADMINS = []  # Your admin users here

def decode_base64(encoded_str):
    try:
        decoded_bytes = base64.b64decode(encoded_str)
        return decoded_bytes.decode('utf-8')
    except Exception as e:
        return f"Error decoding string: {e}"

def decrypt(enc):
    try:
        enc = base64.b64decode(enc.split(':')[0] + '==')
        key = '638udh3829162018'.encode('utf-8')
        iv = 'fedcba9876543210'.encode('utf-8')
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(enc), AES.block_size)
        return plaintext.decode('utf-8')
    except Exception as e:
        return f"Error decrypting: {e}"

@Client.on_message(filters.command("api") & (filters.chat(sudo_group) | filters.user(ADMINS)))
async def start(bot, m):
    # Request API URL
    editable = await bot.send_message(m.chat.id, "**🌐 Enter API URL:**")
    input01 = await bot.listen(editable.chat.id)
    raw_text05 = input01.text.strip()
    await editable.edit("**🔑 Send Token or ID & Password:**")
    input02 = await bot.listen(editable.chat.id)
    raw_text = input02.text.strip()
    await input01.delete(True)
    await input02.delete(True)

    # Login data
    login_hdr = {
        'Client-Service': 'Appx',
        'Auth-Key': 'appxapi',
        'User-ID': '-2',
        'language': 'en',
        'device_type': 'ANDROID',
        'User-Agent': 'okhttp/4.9.1',
        'Host': raw_text05,
    }

    try:
        if "*" in raw_text:
            email, password = raw_text.split("*")
            data = {'email': email, 'password': password}
            scraper = cloudscraper.create_scraper()
            response = scraper.post(f"https://{raw_text05}/post/userLogin", data=data, headers=login_hdr).content
            output = json.loads(response)
            token = output["data"]["token"]
            userid = output["data"]["userid"]
        else:
            token, userid = raw_text.split("$")

        hdr = {
            **login_hdr,
            'Authorization': token,
            'User-ID': userid,
        }

        # Confirm Login Success
        await editable.edit("✅ **Login Successful! Fetching courses...**")

        # Fetch courses
        scraper = cloudscraper.create_scraper()
        course_response = scraper.get(f"https://{raw_text05}/get/mycourse?userid={userid}", headers=hdr).content
        output1 = json.loads(course_response)
        topicid = output1.get("data", [])

        if not topicid:
            await editable.edit("❌ No courses found!")
            return

        cool = ""
        for data in topicid:
            cool += f"`{data['id']}` » {data['course_name']} ★ ₹{data['price']}\n\n"

        await editable.edit(f"**Batches Available:**\n\n{cool}\n\nSEND ID:")
        input1 = await bot.listen(editable.chat.id)
        raw_text1 = input1.text.strip()

        # Process selected course
        course_title = ""
        for data in topicid:
            if data['id'] == raw_text1:
                course_title = data['course_name'].replace('/', '')
                break

        if not course_title:
            await editable.edit("❌ Invalid course ID.")
            return

        await editable.edit(f"**📥 Fetching subjects for course:** {course_title}")

        html3 = scraper.get(f"https://{raw_text05}/get/allsubjectfrmlivecourseclass?courseid={raw_text1}", headers=hdr).content
        output3 = json.loads(html3)
        subject_data = output3.get("data", [])

        total_links = 0
        file_name = f"{course_title}.txt"

        with open(file_name, "w") as f:
            for topic in subject_data:
                subject_title = topic["subject_name"].replace(":", "")
                subject_id = topic["subjectid"]

                html4 = scraper.get(f"https://{raw_text05}/get/alltopicfrmlivecourseclass?courseid={raw_text1}&subjectid={subject_id}", headers=hdr).content
                output4 = json.loads(html4)
                topics = output4.get("data", [])

                for topic_item in topics:
                    topic_id = topic_item['topicid']

                    html5 = scraper.get(f"https://{raw_text05}/get/livecourseclassbycoursesubtopconceptapiv3?topicid={topic_id}&courseid={raw_text1}&subjectid={subject_id}", headers=hdr).content
                    output5 = json.loads(html5)
                    videos = output5.get("data", [])

                    for video in videos:
                        video_title = video["Title"].strip()
                        video_link = video.get("download_link")

                        if video_link:
                            decrypted_link = decrypt(video_link)
                            f.write(f"({subject_title}) {video_title}: {decrypted_link}\n")
                            total_links += 1
                        else:
                            video_id = video["id"]
                            video_detail_response = scraper.get(f"https://{raw_text05}/get/fetchVideoDetailsById?course_id={raw_text1}&video_id={video_id}", headers=hdr).content
                            video_details = json.loads(video_detail_response)
                            encrypted_links = video_details["data"].get("encrypted_links", [])

                            for link in encrypted_links:
                                path = decrypt(link["path"])
                                key = decrypt(link.get("key", ""))
                                key_decoded = decode_base64(key) if key else "No Key"
                                f.write(f"({subject_title}) {video_title}: {path} * {key_decoded}\n")
                                total_links += 1

        caption = f"**🌐 Batch ID:** {raw_text1}\n**📂 Batch:** `{course_title}`\n**🔗 Total Links:** {total_links}\n**📅 Date:** {time}"
        file_media = InputMediaDocument(file_name, caption=caption)

        # Send file
        await bot.send_document(my_data, file_name, caption=caption)
        await bot.send_document(m.chat.id, file_name, caption=caption)

        os.remove(file_name)
        await editable.edit("✅ Batch Grabbing Done!")

    except Exception as e:
        await editable.edit(f"❌ Error: {e}")
