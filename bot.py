#!/usr/bin/env python3
import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ALLOWED_GROUP_ID = int(os.getenv("ALLOWED_GROUP_ID", "0"))
OWNER_USER_ID = int(os.getenv("OWNER_USER_ID", "0"))

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def ai_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    if ALLOWED_GROUP_ID and chat.id != ALLOWED_GROUP_ID:
        return

    if OWNER_USER_ID and user.id != OWNER_USER_ID:
        await update.message.reply_text("Sirf aap hi is command ko use kar sakte hain.")
        return

    if not context.args:
        await update.message.reply_text("Usage: /ai <aapka sawal>")
        return

    question = " ".join(context.args)
    await update.message.chat.send_action(action="typing")

    try:
        response = model.generate_content(question)
        reply = response.text or "Koi jawab nahi mila."
        await update.message.reply_text(reply[:4000])
    except Exception as e:
        await update.message.reply_text("Error: " + str(e))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Super AI ready! Sirf group mein /ai <sawal> use karein.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ai", ai_command))
    app.run_polling()

if __name__ == "__main__":
    main()
