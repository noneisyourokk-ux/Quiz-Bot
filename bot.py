import json
import asyncio
from pyrogram import Client

# ⚙️ अपनी डिटेल्स यहाँ दर्ज करें
API_ID = 12345678  # अपना API ID डालें
API_HASH = "YOUR_API_HASH"  # अपना API Hash डालें
BOT_TOKEN = "YOUR_BOT_TOKEN"  # अपना Bot Token डालें
CHANNEL_ID = "@your_channel_username"  # अपने चैनल का यूज़रनेम या ID (जैसे -100xxx)

app = Client("quiz_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def upload_daily_quiz():
    async with app:
        print("🚀 Quiz Uploading Started...")
        
        # JSON फ़ाइल से सवाल लोड करना
        try:
            with open("questions.json", "r", encoding="utf-8") as file:
                questions_db = json.load(file)
        except Exception as e:
            print(f"❌ Error loading questions.json: {e}")
            return

        for index, item in enumerate(questions_db, start=1):
            try:
                # Telegram Quiz Poll भेजना
                await app.send_poll(
                    chat_id=CHANNEL_ID,
                    question=item["question"],
                    options=item["options"],
                    type="quiz",
                    correct_option_id=item["correct_id"],
                    is_anonymous=True
                )
                print(f"✅ [{index}/{len(questions_db)}] Quiz Posted Successfully!")
                
                # FloodWait / Limit से बचने के लिए 3 सेकंड का गैप
                await asyncio.sleep(3)
                
            except Exception as e:
                print(f"⚠️ Error on Question {index}: {e}")
                await asyncio.sleep(5)
                
        print("\n🎉 All Quizzes Uploaded Successfully!")

if __name__ == "__main__":
    app.run(upload_daily_quiz())