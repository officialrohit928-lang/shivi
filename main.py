import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
    CallbackQuery
)
from pytgcalls import PyTgCalls, idle

# ───── ENV CONFIG ─────
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SESSION_STRING = os.getenv("SESSION_STRING")  # assistant session
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

# ───── BOT CLIENT ─────
bot = Client(
    "shivi_music_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ───── ASSISTANT CLIENT (USER) ─────
assistant = Client(
    session_name="shivi_assistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

# ───── VC CLIENT ─────
vc = PyTgCalls(assistant)

# ───── START MENU ─────
START_TEXT = """
🎧 **SHIVI X VC MUSIC BOT** 🎶

➤ Voice chat music supported  
➤ Assistant auto joins VC  
➤ Use buttons for help

Powered by **Shivi X**
"""

MAIN_MENU = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("ADMIN", callback_data="admin"),
        InlineKeyboardButton("AUTH", callback_data="auth"),
        InlineKeyboardButton("BROADCAST", callback_data="broadcast")
    ],
    [
        InlineKeyboardButton("PLAY", callback_data="play"),
        InlineKeyboardButton("G-BAN", callback_data="gban"),
        InlineKeyboardButton("BLACKLIST", callback_data="blacklist")
    ],
    [
        InlineKeyboardButton("VC-TOOLS", callback_data="vc"),
        InlineKeyboardButton("LOGS", callback_data="logs"),
        InlineKeyboardButton("WELCOME", callback_data="welcome")
    ],
    [
        InlineKeyboardButton("MODERATION", callback_data="moderation"),
        InlineKeyboardButton("PROMOTE", callback_data="promote"),
        InlineKeyboardButton("SETUP", callback_data="setup")
    ]
])

BACK = InlineKeyboardMarkup(
    [[InlineKeyboardButton("⬅️ BACK", callback_data="back")]]
)

HELP_TEXT = {
    "admin": "👮 Admin\n/addadmin\n/deladmin",
    "auth": "🔐 Auth\n/auth\n/unauth",
    "broadcast": "📢 /broadcast",
    "play": "🎵 VC Music\n/play song\n/stop",
    "gban": "🌍 /gban\n/ungban",
    "blacklist": "🚫 /blacklist\n/unblacklist",
    "vc": "🎙️ VC Tools\n/play\n/stop",
    "logs": "📄 /logs",
    "welcome": "👋 /setwelcome",
    "moderation": "🛡️ /ban\n/mute",
    "promote": "⬆️ /promote\n/demote",
    "setup": "⚙️ /settitle"
}

# ───── START COMMAND ─────
@bot.on_message(filters.command("start"))
async def start(_, m: Message):
    await m.reply(
        START_TEXT,
        reply_markup=MAIN_MENU
    )

# ───── VC PLAY ─────
@bot.on_message(filters.command("play") & filters.group)
async def play(_, m: Message):
    if len(m.command) < 2:
        return await m.reply("❌ Song name likho")

    chat_id = m.chat.id
    song = " ".join(m.command[1:])

    await m.reply(f"🎧 **VC join ho raha hai**\n🎵 `{song}`")

    try:
        await vc.join_group_call(
            chat_id,
            audio="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
        )
    except Exception as e:
        await m.reply(f"❌ VC Error:\n`{e}`")

# ───── VC STOP ─────
@bot.on_message(filters.command("stop") & filters.group)
async def stop(_, m: Message):
    try:
        await vc.leave_group_call(m.chat.id)
        await m.reply("⏹️ VC leave kar diya")
    except:
        await m.reply("❌ VC active nahi hai")

# ───── FAKE ADMIN / OTHER COMMANDS (STRUCTURE READY) ─────
@bot.on_message(filters.command("broadcast"))
async def broadcast(_, m: Message):
    if m.from_user.id != OWNER_ID:
        return await m.reply("❌ Owner only")
    await m.reply("📢 Broadcast sent (demo)")

@bot.on_message(filters.command("gban"))
async def gban(_, m: Message):
    await m.reply("🚫 User globally banned (demo)")

# ───── CALLBACK HANDLER ─────
@bot.on_callback_query()
async def callbacks(_, q: CallbackQuery):
    if q.data == "back":
        await q.message.edit(
            START_TEXT,
            reply_markup=MAIN_MENU
        )
    else:
        await q.message.edit(
            HELP_TEXT.get(q.data, "No data"),
            reply_markup=BACK
        )
    await q.answer()

# ───── MAIN RUNNER ─────
async def main():
    await assistant.start()
    await vc.start()
    await bot.start()
    print("🔥 Shivi VC Music Bot Started")
    await idle()

if __name__ == "__main__":
    asyncio.run(main())
