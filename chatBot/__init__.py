from pyrogram import Client
from setup import guu

Soham = Client(
    name="OpenaiBot",api_id=guu.api_id,
    api_hash=guu.api_hash,
    bot_token=guu.bot_token
)
