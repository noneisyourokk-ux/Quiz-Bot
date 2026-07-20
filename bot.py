import os
import json
import asyncio
from pyrogram import Client

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
# CHANNEL_ID अगर स्ट्रिंग है (@username) तो वैसा रहेगा, अगर नंबर है तो int में बदलेगा
RAW_CHANNEL = os.environ.get("CHANNEL_ID")
CHANNEL_ID = int(RAW_CHANNEL) if RAW_CHANNEL.startswith("-100") or RAW_CHANNEL.isdigit() else RAW_CHANNEL

app = Client("quiz_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def upload_daily_quiz():
    async with app:
        print("🚀 Quiz Uploading Started...")
        
        # Peer Sync करने के लिए सबसे पहले चैनल की डिटेल्स लाएं
        try:
            chat = await app.get_chat(CHANNEL_ID)
            target_chat_id = chat.id
            print(f"Connected to Channel: {chat.title} ({target_chat_id})")
        except Exception as e:
            print(f"❌ Channel ID connect error: {e}")
            print("कृपया पक्का करें कि बॉट चैनल में Admin है!")
            return

        # JSON फ़ाइल से सवाल पढ़ना
        try:
            with open("questions.json", "r", encoding="utf-8") as file:
                questions_db = json.load(file)
        except Exception as e:
            print(f"❌ Error loading questions.json: {e}")
            return

        for index, item in enumerate(questions_db, start=1):
            try:
                await app.send_poll(
                    chat_id=target_chat_id,
                    question=item["question"],
                    options=item["options"],
                    type="quiz",
                    correct_option_id=item["correct_id"],
                    is_anonymous=True
                )
                print(f"✅ [{index}/{len(questions_db)}] Quiz Posted Successfully!")
                await asyncio.sleep(3)
                
            except Exception as e:
                print(f"⚠️ Error on Question {index}: {e}")
                await asyncio.sleep(5)
                
        print("\n🎉 All Quizzes Uploaded Successfully!")

if __name__ == "__main__":
    app.run(upload_daily_quiz())
