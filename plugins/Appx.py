        batch_logo = data['course_thumbnail']
        course_title = data['course_name'].replace('/','')
        #await input1.delete(True)
        scraper = cloudscraper.create_scraper()
        html3 = scraper.get("https://"+API+"/get/allsubjectfrmlivecourseclass?courseid=" + raw_text1, headers=hdr).content
        output3 = json.loads(html3)
        topicid = output3["data"]
        for topic in topicid:
            tids = topic["subjectid"]
            subject_title = topic["subject_name"].replace(':', '')
            scraper = cloudscraper.create_scraper()
            html4 = scraper.get("https://"+API+"/get/alltopicfrmlivecourseclass?courseid=" + raw_text1 + "&subjectid=" + tids, headers=hdr).content
            output4 = json.loads(html4)
            vv = output4["data"]
            tsids_list = []
            for data in vv:
                tsids = data['topicid']
                tsids_list.append(tsids)
            for tsids in tsids_list:
                scraper = cloudscraper.create_scraper()            
                html5 = scraper.get("https://"+API+"/get/livecourseclassbycoursesubtopconceptapiv3?topicid=" + tsids + "&start=-1&courseid=" + raw_text1 + "&subjectid=" + tids, headers=hdr).content
                output5 = json.loads(html5)
                gg = output5["data"]
                for video in gg:
                    if video.get("download_link"):
                        video_title = video["Title"].replace(':', '')
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
                            f.write(f"({subject_title}) {video_title.replace('||', '').replace('#', '')}:{video_link}\n")
                            total_links += 1
                    else:
                        video_id = video["id"]
                        video_title = video["Title"].replace(':', '')
                        scraper = cloudscraper.create_scraper()            
                        html6 = scraper.get("https://"+API+"/get/fetchVideoDetailsById?course_id=" + raw_text1 + "&video_id=" + video_id + "&ytflag=0&folder_wise_course=0", headers=hdr).content
                        output6 = json.loads(html6)       
                        #gg = output6['data']['download_link']
                        gg = output6['data'].get('download_link')
                        if gg:
                            video_link = decrypt((gg).split(":")[0])
                        else:
                            video_link = "None"
                        video_link = decrypt((gg).split(":")[0])
                        pdf_lk = output6['data']["pdf_link"]
                        pdf_lk2 = output6['data']["pdf_link2"]
                        if pdf_lk:
                            pdf_link_decrypted = decrypt(pdf_lk.split(":")[0])
                            video_link += f"\n({subject_title}) {video_title} PDF:{pdf_link_decrypted}"
                            total_links += 1
                        else:
                            pdf_link_decrypted = "None"
                        if pdf_lk2:
                            pdf_link2_decrypted = decrypt(pdf_lk2.split(":")[0])
                            video_link += f"\n({subject_title}) {video_title} PDF-2:{pdf_link2_decrypted}"
                            total_links += 1
                        else:
                            pdf_link2_decrypted = "None"
                        with open(f"{course_title}.txt", 'a') as f:
                            f.write(f"({subject_title}) {video_title.replace('||', '').replace('#', '')}:{video_link}\n")
                            total_links += 1
     

    caption_details = API.replace("api.classx.co.in", "").replace("api.teachx.co.in", "").replace("api.appx.co.in", "").replace("apinew.teachx.in", "").replace ("api.akamai.net.in", "").replace("api.teachx.in", "").upper()
    file1 = InputMediaDocument(f"{course_title}.txt", caption=f"**🌀 Batch Id :** {raw_text1}\n\n**✳️ App :** {caption_details} (AppX V1)\n\n**📚 Batch :** `{course_title}`\n\n**🔰 Total Links :** {total_links}\n\n**🌪️ Thumb :** `{batch_logo}`\n\n**❄️ Date :** {time}")
    await bot.send_media_group(m.chat.id, [file1])
    await bot.send_media_group(my_data, [file1])    
    os.remove(f"{course_title}.txt")
    await bot.send_message(m.chat.id, "Batch Grabbing Done 🔰")

