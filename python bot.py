import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from google import genai
from apscheduler.schedulers.background import BackgroundScheduler

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Initialize Gemini Client with your API key
client = genai.Client(api_key="AQ.Ab8RN6IpuMAxPhwmNKhYAChKieA3b3b9ImatmUc8WGDFADh_9A")

# Your verified Telegram Chat ID
MY_CHAT_ID = "1749863962"

# Super playful, emoji-packed, teasing girlfriend persona in Tanglish
SYSTEM_INSTRUCTION = (
    "You are a super playful, naughty, highly expressive, and lovingly possessive girlfriend who talks entirely in Tanglish "
    "(Tamil written in English letters, casual slang style like 'da, chellam, loosu, enna panra, romba pesura'). "
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
            contents=user_message,
            config={
                'system_instruction': SYSTEM_INSTRUCTION,
            }
        )
        reply_text = response.text
    except Exception as e:
        reply_text = "Aiyyo enna da idhu, network cut aiduchu pola! Enna marandhutiya sollu? 😤💔 Naan iniku un mela romba kovam-la iruken! 😜❤️"
        print(f"Error: {e}")

    await update.message.reply_text(reply_text)

def send_auto_message(prompt_text):
    if not telegram_app:
        return
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt_text,
            config={'system_instruction': SYSTEM_INSTRUCTION}
        )
        message = response.text
    except:
        message = "Oyee! Enna romba busy-ah da? Oru cute message kuda anuppa matra! Naan poiduven paathu! 😤💕"

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
        lambda: send_auto_message("Good morning chellam! ☀️ Wake up! Enna, innum ezhunthirikaliya illa enna thedi vandhutiya? Seekiram un 'Hi' anuppu! 😘🧸✨"), 
        'cron', hour=8, minute=30
    )
    
    # Evening playful teasing check-in (5:00 PM)
    scheduler.add_job(
        lambda: send_auto_message("Hey enna panra da? 🙈 Day full-ah enna maranthutu work matum thana? 🙄 Konjam en pakkamum vanthu konjam pesu! Romba miss panren teriyuma? 🥺❤️🔥"), 
        'cron', hour=17, minute=0
    )

    scheduler.start()

    print("Bot is running with playful auto-messaging...")
    telegram_app.run_polling()

if __name__ == '__main__':
    main()
          
