import os
import json
import asyncio
from pyrogram import Client

# Render के Environment Variables से वैल्यू पढ़ना
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

app = Client("quiz_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def upload_daily_quiz():
    async with app:
        print("🚀 Quiz Uploading Started...")
        
        try:
            with open("questions.json", "r", encoding="utf-8") as file:
                questions_db = json.load(file)
        except Exception as e:
            print(f"❌ Error loading questions.json: {e}")
            return

        for index, item in enumerate(questions_db, start=1):
            try:
                await app.send_poll(
                    chat_id=CHANNEL_ID,
                    question=item["question"],
                    options=item["options"],
                    type="quiz",
                    correct_option_id=item["correct_id"],
                    is_anonymous=True
                )
                print(f"✅ [{index}/{len(questions_db)}] Quiz Posted Successfully!")
                await asyncio.sleep(3)  # 3 second gap
                
            except Exception as e:
                print(f"⚠️ Error on Question {index}: {e}")
                await asyncio.sleep(5)
                
        print("\n🎉 All Quizzes Uploaded Successfully!")

if __name__ == "__main__":
    app.run(upload_daily_quiz())