import time
import math
import os
from pyrogram.errors import FloodWait
from datetime import datetime,timedelta


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#

def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#

def hrb(value, digits= 2, delim= "", postfix=""):
    """Return a human-readable file size.
    """
    if value is None:
        return None
    chosen_unit = "B"
    for unit in ("KB", "MB", "GB", "TB"):
        if value > 1000:
            value /= 1024
            chosen_unit = unit
        else:
            break
    return f"{value:.{digits}f}" + delim + chosen_unit + postfix

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#    
    
def hrt(seconds, precision = 0):
    """Return a human-readable time delta as a string.
    """
    pieces = []
    value = timedelta(seconds=seconds)
    

    if value.days:
        pieces.append(f"{value.days}d")

    seconds = value.seconds

    if seconds >= 3600:
        hours = int(seconds / 3600)
        pieces.append(f"{hours}h")
        seconds -= hours * 3600

    if seconds >= 60:
        minutes = int(seconds / 60)
        pieces.append(f"{minutes}m")
        seconds -= minutes * 60

    if seconds > 0 or not pieces:
        pieces.append(f"{seconds}s")

    if not precision:
        return "".join(pieces)

    return "".join(pieces[:precision])

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#

class Timer:
    def __init__(self, time_between=3):
        self.start_time = time.time()
        self.time_between = time_between

    def can_send(self):
        if time.time() > (self.start_time + self.time_between):
            self.start_time = time.time()
            return True
        return False

timer = Timer()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------#

async def progress_bar(current, total, reply, start):
    if timer.can_send():
        now = time.time()
        diff = now - start
        if diff < 1:
            return
        else:
            perc = f"{current * 100 / total:.1f}%"
            elapsed_time = round(diff)
            speed = current / elapsed_time
            sp = str(hrb(speed)) + "ps"
            tot = hrb(total)
            cur = hrb(current)
            eta = timedelta(seconds=(total - current) / speed)
            eta_str = hrt(eta.total_seconds(), precision=2)

            # Calculate the number of filled and empty blocks in the progress bar
            filled_blocks = round(current / total * 13)
            empty_blocks = 13 - filled_blocks

            # Construct the progress bar
            bar = "▰" * filled_blocks + "▱" * empty_blocks

            try:
                # Add flashing emoji for ETA time
                flash_emoji = "⚡" * (int(diff) % 2 == 0)
                await reply.edit(
                    f"╭──⌈📥 𝙐𝙥𝙡𝙤𝙖𝙙𝙞𝙣𝙜 𝙑𝙞𝙙𝙚𝙤𝙨⌋──╮\n"
                    f"├ {bar} \n"
                    f"├ 𝙎𝙥𝙚𝙚𝙙 **:** {sp} \n"
                    f"├ 𝙋𝙧𝙤𝙜𝙧𝙚𝙨𝙨 **:** {perc} \n"
                    f"├ 𝙎𝙞𝙯𝙚 **:** {cur} **/** {tot} \n"
                    f"├ 𝙀𝙏𝘼 **:** {eta_str} {flash_emoji} \n"
                    f"├ {bar} \n"
                    f"╰───⌈ 𝐑𝐄𝐗𝐎 𝐁𝐎𝐓 🚨 ⌋────╯\n"
                )

            except FloodWait as e:
                time.sleep(e.x)
