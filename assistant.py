from pyrogram import Client
import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")

assistant = Client(
    session_name="assistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)
