import subprocess
import datetime
import asyncio
import math
import tgcrypto
from typing import Union
import os
import requests
import time
from handlers.p_bar import progress_bar
import aiohttp
import aiofiles
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram import Client, filters
from pyrogram import Client as bot
from subprocess import getstatusoutput

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#

def duration(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    try:
        return float(result.stdout.strip())
    except (ValueError, TypeError):
        if b"EBML header parsing failed" in result.stdout:
            return None
        else:
            raise

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#

async def aio(url, name):
    filename = f'{name}'
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=10) as resp:
                if resp.status != 200:
                    raise ValueError(f'Request failed with status {resp.status}')
                async with aiofiles.open(filename, mode='wb') as f:
                    async for chunk in resp.content.iter_chunked(8192):
                        await f.write(chunk)
                return filename
        except (aiohttp.ClientError, OSError, ValueError) as e:
            print(f'Error downloading {url}: {e}')
            return None

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#

def vid_info(info):
    info = info.strip()
    info = info.split("\n")
    new_info = dict()
    temp = []
    for i in info:
        i = str(i)
        if "[" not in i and '---' not in i:
            while "  " in i:
                i = i.replace("  ", " ")
            i.strip()
            i = i.split("|")[0].split(" ",3)
            try:
                if "RESOLUTION" not in i[2] and i[2] not in temp and "audio" not in i[2]:
                    temp.append(i[2])
                    
                    # temp.update(f'{i[2]}')
                    # new_info.append((i[2], i[0]))
                    #  mp4,mkv etc ==== f"({i[1]})" 
                    
                    new_info.update({f'{i[2]}':f'{i[0]}'})

            except:
                pass
    return new_info

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#

async def run(cmd):
    try:
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)

        stdout, stderr = await proc.communicate()

        print(f'[{cmd!r} exited with {proc.returncode}]')
        if proc.returncode == 1:
            return False
        if stdout:
            return f'[stdout]\n{stdout.decode()}'
        if stderr:
            return f'[stderr]\n{stderr.decode()}'
    except asyncio.TimeoutError:
        print(f"[{cmd!r} timed out]")
        return False
    except Exception as e:
        print(f"[{cmd!r} failed with exception: {e}]")
        return False

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#         

def human_readable_size(size, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if size < 1024.0 or unit == 'PB':
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#

def time_name():
    date = datetime.date.today()
    now = datetime.datetime.now()
    current_time = now.strftime("%H%M%S")
    return f"{date} {current_time}.mp4"

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#
async def download_video(url, cmd, name):
    download_cmd = f"{cmd} -R 25 --fragment-retries 25 --external-downloader aria2c --downloader-args 'aria2c: -x 16 -j 32'"
    print(download_cmd)
    k = subprocess.run(download_cmd, shell=True)
    if "visionias" in cmd and k.returncode != 0:
        await asyncio.sleep(5)
        await download_video(url, cmd, name)
    try:
        video_extensions = [".webm", ".mkv", ".mp4", ".mp4.webm"]
        for ext in video_extensions:
            video_path = os.path.join(os.getcwd(), f"{name}{ext}")
            if os.path.isfile(video_path):
                return video_path
        raise FileNotFoundError(f"No video file found for {name}")
    except Exception as exc:
        print(f"Error: {exc}")
        return os.path.join(os.getcwd(), f"{name}.mp4")
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#

async def send_vid(bot: Client, m: Message, cc, filename, thumb, name, prog):
    
    subprocess.run(f'ffmpeg -i "{filename}" -ss 00:00:12 -vframes 1 "{filename}.jpg"', shell=True)
    await prog.delete(True)
    reply = await bot.send_message(m.chat.id, f"**Uploading Video :- ** `{name}`")
    try:
        if thumb == "no" or thumb == "n" or thumb == "N" or thumb == "No" or thumb == "NO":
            thumbnail = f"{filename}.jpg"
        else:
            thumbnail = thumb
    except Exception as e:
        await m.reply_text(str(e))

    dur = int(duration(filename))
    start_time = time.time()
    try:
        await bot.send_video(m.chat.id, filename, caption=cc, supports_streaming=True, height=720, width=1280, thumb=thumbnail, duration=dur, progress=progress_bar, progress_args=(reply,start_time))
    except Exception:
        await bot.send_video(m.chat.id, filename, caption=cc, supports_streaming=True, height=720, width=1280, thumb=thumbnail, duration=dur, progress=progress_bar, progress_args=(reply,start_time))
    
    os.remove(filename)
    os.remove(f"{filename}.jpg")
    await prog.delete(True)
    await reply.delete(True)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#
    
def get_video_attributes(file: str):
    """Returns video duration, width, height"""

    class FFprobeAttributesError(Exception):
        """Exception if ffmpeg fails to generate attributes"""

    cmd = (
        "ffprobe -v error -show_entries format=duration "
        + "-of default=noprint_wrappers=1:nokey=1 "
        + "-select_streams v:0 -show_entries stream=width,height "
        + f" -of default=nw=1:nk=1 '{file}'"
    )
    res, out = getstatusoutput(cmd)
    if res != 0:
        raise FFprobeAttributesError(out)
    width, height, dur = out.split("\n")
    return (int(float(dur)), int(width), int(height))
