import asyncio
import time
from telethon import TelegramClient, events

API_ID = "28992023"
API_HASH = "72402a966addaa945e14cebbd9cb82fd"
SESSION_NAME = "session"

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

last_reply_time = {}

async def is_user_offline():
    """Check if the user is offline by fetching their last seen status."""
    me = await client.get_me()
    me_status = await client.get_entity(me.id)
    
    if me_status.status is None:  # If status is None, you're offline
        return True  
    return False

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
client.run_until_disconnected()
