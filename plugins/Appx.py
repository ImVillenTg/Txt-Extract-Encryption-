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
    file1 = InputMediaDocument(f"{course_title}.txt", caption=f"࿇ ══━━𝐑𝐄𝐗𝐎𝐃𝐀𝐒━━══ ࿇\n\n**🌀 Batch Id :** {raw_text1}\n\n**✳️ App :** {caption_details} (AppX V1)\n\n**📚 Batch :** `{course_title}`\n\n**🔰 Total Links :** {total_links}\n\n**🌪️ Thumb :** `{batch_logo}`\n\n**❄️ Date :** {time}")
    await bot.send_media_group(m.chat.id, [file1])
    await bot.send_media_group(my_data, [file1])    
    os.remove(f"{course_title}.txt")
    await bot.send_message(m.chat.id, "Batch Grabbing Done 🔰")
