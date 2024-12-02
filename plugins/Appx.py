# Debugged Appx.py to ensure extraction and writing
import json
import requests
from pyrogram.types import InputMediaDocument
from pyrogram import Client, filters
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import os
import cloudscraper
import datetime

# Configurations
time = datetime.datetime.now().strftime("%d-%m-%Y")
my_data = -1001938939742  # Example Group ID
sudo_group = []  # Your sudo group here
ADMINS = []  # Your admin users here

# Utility functions
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
    # Step 1: Get API URL and login details
    editable = await bot.send_message(m.chat.id, "**🌐 Enter API URL:**")
    input01 = await bot.listen(editable.chat.id)
    api_url = input01.text.strip()
    await editable.edit("**🔑 Send Token or ID & Password:**")
    input02 = await bot.listen(editable.chat.id)
    login_details = input02.text.strip()
    await input01.delete()
    await input02.delete()

    # Step 2: Login and fetch token/userid
    login_hdr = {
        'Client-Service': 'Appx',
        'Auth-Key': 'appxapi',
        'User-ID': '-2',
        'language': 'en',
        'device_type': 'ANDROID',
        'User-Agent': 'okhttp/4.9.1',
        'Host': api_url,
    }

    try:
        if "*" in login_details:
            email, password = login_details.split("*")
            data = {'email': email, 'password': password}
            scraper = cloudscraper.create_scraper()
            response = scraper.post(f"https://{api_url}/post/userLogin", data=data, headers=login_hdr).content
            output = json.loads(response)
            token = output["data"]["token"]
            userid = output["data"]["userid"]
        else:
            token, userid = login_details.split("$")

        hdr = {
            **login_hdr,
            'Authorization': token,
            'User-ID': userid,
        }

        await editable.edit("✅ **Login Successful! Fetching courses...**")

        # Step 3: Fetch courses
        scraper = cloudscraper.create_scraper()
        course_response = scraper.get(f"https://{api_url}/get/mycourse?userid={userid}", headers=hdr).content
        courses = json.loads(course_response).get("data", [])

        if not courses:
            await editable.edit("❌ No courses found!")
            return

        course_list = "\n".join([f"`{c['id']}` » {c['course_name']} ★ ₹{c['price']}" for c in courses])
        await editable.edit(f"**Available Courses:**\n\n{course_list}\n\nSEND COURSE ID:")
        input_course = await bot.listen(editable.chat.id)
        selected_course_id = input_course.text.strip()

        # Step 4: Fetch course details
        course_title = next((c['course_name'] for c in courses if c['id'] == selected_course_id), "Unknown Course").replace('/', '')
        if course_title == "Unknown Course":
            await editable.edit("❌ Invalid course ID.")
            return

        subjects_response = scraper.get(f"https://{api_url}/get/allsubjectfrmlivecourseclass?courseid={selected_course_id}", headers=hdr).content
        subjects = json.loads(subjects_response).get("data", [])

        if not subjects:
            await editable.edit("❌ No subjects found for the selected course.")
            return

        total_links = 0
        file_name = f"{course_title}.txt"

        # Step 5: Process and extract data
        with open(file_name, "w") as f:
            for subject in subjects:
                subject_id = subject['subjectid']
                subject_name = subject['subject_name'].replace(":", "")

                topics_response = scraper.get(f"https://{api_url}/get/alltopicfrmlivecourseclass?courseid={selected_course_id}&subjectid={subject_id}", headers=hdr).content
                topics = json.loads(topics_response).get("data", [])

                for topic in topics:
                    topic_id = topic['topicid']

                    videos_response = scraper.get(f"https://{api_url}/get/livecourseclassbycoursesubtopconceptapiv3?courseid={selected_course_id}&subjectid={subject_id}&topicid={topic_id}", headers=hdr).content
                    videos = json.loads(videos_response).get("data", [])

                    for video in videos:
                        video_title = video["Title"].strip()
                        video_link = video.get("download_link")

                        if video_link:
                            decrypted_link = decrypt(video_link)
                            f.write(f"({subject_name}) {video_title}: {decrypted_link}\n")
                            total_links += 1
                        else:
                            video_id = video["id"]
                            video_detail_response = scraper.get(f"https://{api_url}/get/fetchVideoDetailsById?video_id={video_id}", headers=hdr).content
                            video_details = json.loads(video_detail_response).get("data", {})
                            encrypted_links = video_details.get("encrypted_links", [])

                            for link in encrypted_links:
                                path = decrypt(link.get("path", ""))
                                key = decrypt(link.get("key", ""))
                                key_decoded = decode_base64(key) if key else "No Key"
                                f.write(f"({subject_name}) {video_title}: {path} * {key_decoded}\n")
                                total_links += 1

        if total_links == 0:
            await editable.edit("❌ No links were extracted.")
        else:
            caption = f"**🌐 Batch ID:** {selected_course_id}\n**📂 Batch:** `{course_title}`\n**🔗 Total Links:** {total_links}\n**📅 Date:** {time}"
            await bot.send_document(my_data, file_name, caption=caption)
            await bot.send_document(m.chat.id, file_name, caption=caption)
            os.remove(file_name)
            await editable.edit("✅ Batch Grabbing Done!")
    except Exception as e:
        await editable.edit(f"❌ Error: {e}")
