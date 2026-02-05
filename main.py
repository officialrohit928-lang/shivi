import os
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
    CallbackQuery
)

# ───── CONFIG ─────
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

app = Client(
    "shivi_music",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ───── START MENU ─────
START_TEXT = """
❖ **SHIVI X MUSIC BOT** ❖ 💖

➤ Choose category for help  
➤ All commands use with `/`

Powered by @ShiviXMusic
"""

MAIN_MENU = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("ADMIN", callback_data="admin"),
        InlineKeyboardButton("AUTH", callback_data="auth"),
        InlineKeyboardButton("BROADCAST", callback_data="broadcast")
    ],
    [
        InlineKeyboardButton("BLACKLIST", callback_data="blacklist"),
        InlineKeyboardButton("PLAY", callback_data="play"),
        InlineKeyboardButton("G-BAN", callback_data="gban")
    ],
    [
        InlineKeyboardButton("VC-TOOLS", callback_data="vc_tools"),
        InlineKeyboardButton("LOGS", callback_data="logs"),
        InlineKeyboardButton("START", callback_data="start_help")
    ],
    [
        InlineKeyboardButton("ACTION", callback_data="action"),
        InlineKeyboardButton("MODERATION", callback_data="moderation"),
        InlineKeyboardButton("SETUP", callback_data="setup")
    ],
    [
        InlineKeyboardButton("WELCOME", callback_data="welcome"),
        InlineKeyboardButton("VC-LOGGER", callback_data="vc_logger"),
        InlineKeyboardButton("PROMOTE", callback_data="promote")
    ]
])

BACK_BTN = InlineKeyboardMarkup(
    [[InlineKeyboardButton("⬅️ BACK", callback_data="back")]]
)

# ───── COMMANDS ─────
@app.on_message(filters.command("start"))
async def start_cmd(_, message: Message):
    await message.reply_photo(
        photo="https://telegra.ph/file/3a0f2f5f1c4d2d1e1f5e4.jpg",
        caption=START_TEXT,
        reply_markup=MAIN_MENU
    )

@app.on_message(filters.command("play"))
async def play_cmd(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("🎵 **Song name do bhai**")
    song = " ".join(message.command[1:])
    await message.reply(f"▶️ **Playing:** `{song}`")

@app.on_message(filters.command("pause"))
async def pause_cmd(_, message: Message):
    await message.reply("⏸️ Music paused")

@app.on_message(filters.command("resume"))
async def resume_cmd(_, message: Message):
    await message.reply("▶️ Music resumed")

@app.on_message(filters.command("stop"))
async def stop_cmd(_, message: Message):
    await message.reply("⏹️ Music stopped")

# ───── CALLBACK HANDLER ─────
@app.on_callback_query()
async def cb_handler(_, query: CallbackQuery):
    data = query.data

    HELP_TEXTS = {
        "admin": "👮 **Admin Commands**\n/addadmin\n/deladmin",
        "auth": "🔐 **Auth Commands**\n/auth\n/unauth",
        "broadcast": "📢 **Broadcast**\n/broadcast",
        "blacklist": "🚫 **Blacklist**\n/blacklist\n/unblacklist",
        "play": "🎵 **Music**\n/play song\n/pause\n/resume\n/stop",
        "gban": "🌍 **Global Ban**\n/gban\n/ungban",
        "vc_tools": "🎙️ **VC Tools**\n/vcmute\n/vcunmute",
        "logs": "📄 **Logs**\n/logs",
        "start_help": "/start – Start bot",
        "action": "⚡ **Actions**\n/pin\n/unpin",
        "moderation": "🛡️ **Moderation**\n/ban\n/mute",
        "setup": "⚙️ **Setup**\n/settitle\n/setphoto",
        "welcome": "👋 **Welcome**\n/setwelcome",
        "vc_logger": "📝 **VC Logger**\n/vclog on/off",
        "promote": "⬆️ **Promote**\n/promote\n/demote"
    }

    if data == "back":
        await query.message.edit_caption(
            caption=START_TEXT,
            reply_markup=MAIN_MENU
        )
    else:
        await query.message.edit_caption(
            caption=HELP_TEXTS.get(data, "No info"),
            reply_markup=BACK_BTN
        )

    await query.answer()

# ───── RUN ─────
print("🔥 Shivi Music Bot Started...")
app.run()
