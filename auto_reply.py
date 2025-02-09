import asyncio
import time
from flask import Flask
from telethon import TelegramClient, events
import os

# Load API credentials from environment variables
API_ID = int(os.getenv("API_ID", "28992023"))  # Replace with your API ID
API_HASH = os.getenv("API_HASH", "72402a966addaa945e14cebbd9cb82fd")  # Replace with your API Hash
SESSION_NAME = "session"

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

last_reply_time = {}

@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    if event.is_private:  # Only reply to private messages
        sender = await event.get_sender()
        sender_id = sender.id

        print(f"Received message from: {sender.first_name} (ID: {sender_id})")

        # Prevent spamming (reply only once per minute)
        current_time = time.time()
        if sender_id in last_reply_time and (current_time - last_reply_time[sender_id] < 60):
            print("Skipping auto-reply to avoid spamming.")
            return  

        last_reply_time[sender_id] = current_time
        reply_message = f"Hey {sender.first_name}, I'm currently busy but I'll get back to you soon!"
        await event.reply(reply_message)
        print(f"Sent auto-reply to {sender.first_name}.")

print("Starting Telegram auto-reply bot...")
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

    # Start Flask web server
    app.run(host="0.0.0.0", port=10000)
