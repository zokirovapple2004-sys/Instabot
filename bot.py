import os
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import yt_dlp

# Telegram bot tokenini Environment Variable orqali olamiz
TOKEN = os.getenv("8521244382:AAGgiPYDyurs5XFPZu85rYUnOG_m242JqBI")

async def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "instagram.com" in url or "tiktok.com" in url:
        msg = await update.message.reply_text("Yuklanmoqda... 🚀")
        try:
            file_path = await asyncio.to_thread(download_video, url)
            with open(file_path, 'rb') as video:
                await update.message.reply_video(video)
            os.remove(file_path) # Faylni o'chiramiz
            await msg.delete()
        except Exception as e:
            await update.message.reply_text(f"Xatolik yuz berdi: {e}")
    else:
        await update.message.reply_text("Iltimos, faqat Instagram yoki TikTok linkini yuboring!")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == '__main__':
    main()
