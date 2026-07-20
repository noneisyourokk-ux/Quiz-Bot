import os
import json
import asyncio
from aiohttp import web
from pyrogram import Client, filters

# ================= CONFIG =================
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID"))

app = Client(
    "quiz_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ================= WEB SERVER =================
async def handle(request):
    return web.Response(text="Quiz Bot is Running!")

async def start_web_server():
    web_app = web.Application()
    web_app.router.add_get("/", handle)

    runner = web.AppRunner(web_app)
    await runner.setup()

    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    print(f"🌐 Web server running on port {port}")

# ================= LOAD QUESTIONS =================
def load_questions():
    with open("questions.json", "r", encoding="utf-8") as f:
        return json.load(f)

# ================= UPLOAD QUIZZES =================
async def upload_quizzes():
    questions = load_questions()

    chat = await app.get_chat(CHANNEL_ID)
    print(f"📢 Connected to: {chat.title}")

    for i, q in enumerate(questions, start=1):
        try:
            await app.send_poll(
                chat_id=CHANNEL_ID,
                question=q["question"],
                options=q["options"],
                type="quiz",
                correct_option_id=q["correct_id"],
                is_anonymous=True,
                explanation="Correct Answer"
            )

            print(f"✅ Quiz {i} uploaded")
            await asyncio.sleep(3)

        except Exception as e:
            print(f"❌ Error in quiz {i}: {e}")
            await asyncio.sleep(5)

# ================= COMMANDS =================
@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    await message.reply_text(
        "🤖 Quiz Bot Active!\n"
        "Use /upload to upload quizzes."
    )

@app.on_message(filters.command("upload"))
async def upload_cmd(client, message):
    await message.reply_text("⏳ Uploading quizzes...")
    await upload_quizzes()
    await message.reply_text("✅ All quizzes uploaded!")

# ================= MAIN =================
async def main():
    await start_web_server()
    await app.start()

    me = await app.get_me()
    print(f"🤖 Logged in as @{me.username}")

    # Startup par automatic upload
    await upload_quizzes()

    print("🚀 Bot is running...")

    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
