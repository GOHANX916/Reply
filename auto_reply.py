from telethon import TelegramClient, events, functions
import time
import os

# Load API credentials (Replace with your actual API_ID and API_HASH or use environment variables)
API_ID = 28992023
API_HASH = "72402a966addaa945e14cebbd9cb82fd"
SESSION_NAME = "session"

# Initialize the Telegram Client
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
last_reply_time = {}

async def disable_online_status():
    """ Prevents Telegram from showing 'online' or 'typing' status """
    await client(functions.account.UpdateStatusRequest(offline=True))

@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    await disable_online_status()  # Hide online status before replying

    if event.is_private:  
        sender = await event.get_sender()
        sender_id = sender.id
        
        current_time = time.time()
        if sender_id in last_reply_time and (current_time - last_reply_time[sender_id] < 3600):
            return  # Don't reply if it's been less than an hour
        
        last_reply_time[sender_id] = current_time
        
        # Hidden bot username in the message
        reply_message = f"Hey {sender.first_name}, I'm offline. I'll reply when I'm back! Till then, [Visit this Bot](https://t.me/haxk_mbot)"
        await event.reply(reply_message, link_preview=False)

print("✅ Auto-reply bot is running...")
client.start()
client.run_until_disconnected()
