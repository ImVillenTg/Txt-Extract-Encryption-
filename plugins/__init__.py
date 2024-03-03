from pyrogram import filters
from pyrogram import Client as bot
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from main import LOGGER, prefixes, AUTH_USERS
import os
import sys
import config
from pyrogram import Client, filters
from handlers import helper
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
from pyromod import listen
from pyrogram.types import Message

ADMINS = config.ADMINS
# DB_URL = config.DB_URL
# DB_NAME = config.DB_NAME
# db = Database(DB_URL, DB_NAME)
sudo_group = config.GROUPS

@bot.on_message(filters.command("start") & filters.private)
async def account_login(bot: Client, m: Message):
    if m.from_user.id not in AUTH_USERS:
        return
    editable = await m.reply_text(f"Hello Bruh 🔥 [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n\n**What's Up !**")

@bot.on_message(filters.command("cancel") & (filters.chat(sudo_group) | filters.user(ADMINS)))
async def restart_handler(_, m):
    if m.from_user.id not in AUTH_USERS:
        return
    await m.reply_text("Stopped 😡!", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command("log") & (filters.chat(sudo_group) | filters.user(ADMINS)))
async def log_msg(bot, m: Message):   
    await bot.send_document(m.chat.id, "log.txt")
