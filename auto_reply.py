from telethon import TelegramClient, events
import time

API_ID = "28992023"
API_HASH = "72402a966addaa945e14cebbd9cb82fd"
SESSION_NAME = "session"

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
last_reply_time = {}

@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    if event.is_private:  
        sender = await event.get_sender()
        sender_id = sender.id
        
        current_time = time.time()
        if sender_id in last_reply_time and (current_time - last_reply_time[sender_id] < 3600):
            return  # Don't reply if it's been less than an hour
        
        last_reply_time[sender_id] = current_time
        reply_message = f"Hey {sender.first_name}, I'm offline. I'll reply when I'm back!"
        await event.reply(reply_message)

print("Auto-reply bot is running...")
client.start()
client.run_until_disconnected()
