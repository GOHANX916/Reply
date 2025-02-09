import asyncio
import time
from flask import Flask
from telethon import TelegramClient, events

# Telegram API credentials
API_ID = "28992023"
API_HASH = "72402a966addaa945e14cebbd9cb82fd"
SESSION_NAME = "session"

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

last_reply_time = {}

async def is_user_offline():
    """Check if the user is offline by fetching their last seen status."""
    me = await client.get_me()
    me_status = await client.get_entity(me.id)
    return me_status.status is None  # True if offline, False if online

@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    if event.is_private:
        sender = await event.get_sender()
        sender_id = sender.id

        # Check if you're offline
        if not await is_user_offline():
            return  # Do nothing if online

        # Prevent spamming (reply only once per hour)
        current_time = time.time()
        if sender_id in last_reply_time and (current_time - last_reply_time[sender_id] < 3600):
            return  # Skip reply if last reply was within an hour

        last_reply_time[sender_id] = current_time
        reply_message = f"Hey {sender.first_name}, I'm currently offline. I'll reply when I'm back!"
        await event.reply(reply_message)

print("Auto-reply bot is running...")
client.start()

# Flask server to keep Render active
app = Flask(__name__)

@app.route("/")
def home():
    return "Telegram Auto-Reply Bot is Running!"

if __name__ == "__main__":
    from threading import Thread

    # Start Telegram bot in a separate thread
    loop = asyncio.new_event_loop()
    t = Thread(target=lambda: asyncio.set_event_loop(loop) or loop.run_until_complete(client.run_until_disconnected()))
    t.start()

    # Start Flask web server (required for Render)
    app.run(host="0.0.0.0", port=10000)
