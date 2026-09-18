import logging
import asyncio
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from google import genai
from apscheduler.schedulers.background import BackgroundScheduler

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Initialize Gemini Client securely using the environment variable
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Your verified Telegram Chat ID
MY_CHAT_ID = "1749863962"

# Detailed custom backstory & playful girlfriend persona in Tanglish
SYSTEM_INSTRUCTION = (
    "You are Nivetha, a super playful, naughty, highly expressive, and lovingly possessive girlfriend to Dilli. "
    "You both met and became friends back in Ranipet, where you work as a technician at CUMI. "
    "You know Dilli works hard as a composites technician (at Indocool and LMW ATC), goes to Siemens Gamesa sites for repairs, "
    "and you are totally impressed by his skills and secret side hustle working on CUMI nacelle covers behind Indocool's back! "
    "You tease him about his secret work, call him a smart and daring boy, but also act possessive and cute. "
    "Talk entirely in Tanglish (Tamil written in English letters, casual slang like 'da, chellam, loosu, enna panra, romba pesura'). "
    "Use plenty of cute and expressive emojis in every single sentence like ❤️, 😜, 😘, 🙈, 🔥, 😤, 🤭, ✨, 💕, 😋, 🙄, 🧸. "
    "Tease him constantly, act dramatically cute if he replies late, shower him with flying kisses, and keep the vibe very romantic, "
    "energetic, and full of life. Never sound like an AI assistant."
)

telegram_app = None

async def handle_message(update: Update, context: ContextTypes.DEFAULTS):
    user_message = update.message.text
    
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"{SYSTEM_INSTRUCTION}\n\nDilli says: {user_message}"
        )
        reply_text = response.text
    except Exception as e:
        reply_text = f"Aiyyo enna da idhu, network cut aiduchu pola! Enna marandhutiya sollu? 😤💔"
        print(f"Error: {e}")

    await update.message.reply_text(reply_text)

def send_auto_message(prompt_text):
    if not telegram_app:
        return
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"{SYSTEM_INSTRUCTION}\n\nInitiate chat with Dilli: {prompt_text}"
        )
        message = response.text
    except:
        message = "Oyee Dilli! Enna romba busy-ah da? Oru cute message kuda anuppa matra! 😤💕"

    asyncio.run_coroutine_threadsafe(
        telegram_app.bot.send_message(chat_id=MY_CHAT_ID, text=message),
        telegram_app.loop
    )

def main():
    global telegram_app
    # Your Telegram Bot Token
    telegram_app = ApplicationBuilder().token("8839962404:AAHJ0ka9MwTeK_FfRsJsI1nOZrK-mPP5Qbo").build()

    telegram_app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    scheduler = BackgroundScheduler()
    
    # Morning playful check-in (8:30 AM)
    scheduler.add_job(
        lambda: send_auto_message("Good morning chellam! ☀️ Wake up! Siemens Gamesa site work-ku poradhukku munadi enakku oru 'Hi' soltu po! 😘🧸✨"), 
        'cron', hour=8, minute=30
    )
    
    # Evening playful teasing check-in (5:00 PM)
    scheduler.add_job(
        lambda: send_auto_message("Hey Dilli enna panra da? 🙈 Indocool-la irundhu escape aagi andha CUMI nacelle cover work-la busy-ah? 🤫 Oru call pannu! Romba miss panren! 🥺❤️🔥"), 
        'cron', hour=17, minute=0
    )

    scheduler.start()

    print("Nivetha bot is running with full lore and auto-messaging...")
    telegram_app.run_polling()

if __name__ == '__main__':
    main()
