import os
import json
import asyncio
from aiohttp import web
from pyrogram import Client

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

RAW_CHANNEL = os.environ.get("CHANNEL_ID")
CHANNEL_ID = int(RAW_CHANNEL) if RAW_CHANNEL.startswith("-100") or RAW_CHANNEL.lstrip('-').isdigit() else RAW_CHANNEL

app = Client("quiz_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Render Web Port Binding के लिए Web Server
async def handle_ping(request):
    return web.Response(text="Bot is Live and Healthy!")

async def start_web_server():
    server = web.Application()
    server.router.add_get('/', handle_ping)
    runner = web.AppRunner(server)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"🌐 Web Server running on port {port}")

async def upload_daily_quiz():
    # Web Server चालू करना
    await start_web_server()
    
    async with app:
        print("🚀 Quiz Uploading Started...")
        
        try:
            chat = await app.get_chat(CHANNEL_ID)
            target_chat_id = chat.id
            print(f"Connected to Channel: {chat.title} ({target_chat_id})")
        except Exception as e:
            print(f"❌ Channel Connect Error: {e}")
            return

        try:
            with open("questions.json", "r", encoding="utf-8") as file:
                questions_db = json.load(file)
        except Exception as e:
            print(f"❌ Error loading questions.json: {e}")
            return

        for index, item in enumerate(questions_db, start=1):
            try:
                # ऑप्शंस को शुद्ध स्ट्रिंग लिस्ट में सुनिश्चित करना
                formatted_options = [str(opt) for opt in item["options"]]

                await app.send_poll(
                    chat_id=target_chat_id,
                    question=str(item["question"]),
                    options=formatted_options,
                    type="quiz",
                    correct_option_id=int(item["correct_id"]),
                    is_anonymous=True
                )
                print(f"✅ [{index}/{len(questions_db)}] Quiz Posted Successfully!")
                await asyncio.sleep(3)
                
            except Exception as e:
                print(f"⚠️ Error on Question {index}: {e}")
                await asyncio.sleep(5)
                
        print("\n🎉 All Quizzes Uploaded Successfully!")

        # Render सर्विस को एक्टिव रखने के लिए लूप
        while True:
            await asyncio.sleep(3600)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(upload_daily_quiz())
