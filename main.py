import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import wikipediaapi


load_dotenv()

TOKEN = os.getenv("TOKEN")


wiki = wikipediaapi.Wikipedia(
    language='uz',
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"  # O'zingizning user agentni kiriting
)


async def start(update: Update, context):
    chat_id = update.message.id
    full_name = update.message.from_user.full_name
    await update.message.reply_text(f"Salom! {full_name} Menga biror mavzu yozing, men Wikipedia'dan ma'lumot topaman.")


async def search(update: Update, context):
    query = update.message.text
    page = wiki.page(query)

    if page.exists():
        summary = page.summary[:2000]
        image_url = page.fullurl
        await update.message.reply_text(f"{summary}\nBatafsil ma'lumot: {image_url}")
    else:
        await update.message.reply_text("Kechirasiz, ushbu mavzu bo'yicha ma'lumot topilmadi.")


if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))

    app.run_polling()

