import os
import asyncio
import threading
from flask import Flask
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from yt_dlp import YoutubeDL

# 1. Flask server (Render botni o'chirib qo'ymasligi uchun)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

# 2. Bot sozlamalari
TOKEN = "8090453345:AAF-kxU8eej7k6BPXjS5q3uGBAvnfWPJyng"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# 3. Video yuklash funksiyasi
def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        # Instagram va TikTok uchun ba'zan kerak bo'ladigan user-agent
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Assalomu alaykum! TikTok yoki Instagram havolasini yuboring, men uni yuklab beraman.")

@dp.message(F.text.contains("instagram.com") | F.text.contains("tiktok.com"))
async def handle_video(message: types.Message):
    status_msg = await message.answer("⏳ Video yuklanmoqda, kuting...")
    
    try:
        # Faylni yuklab olish (alohida oqimda)
        file_path = await asyncio.to_thread(download_video, message.text)
        
        # Videoni yuborish
        video_file = types.FSInputFile(file_path)
        await message.answer_video(video_file, caption="✅ Video yuklab olindi!")
        
        # Serverni tozalash
        os.remove(file_path)
        await status_msg.delete()
        
    except Exception as e:
        await status_msg.edit_text(f"❌ Xatolik yuz berdi. Havola to'g'riligini tekshiring yoki bot keyinroq urinib ko'ring.\n\nTexnik xato: {str(e)[:50]}")

async def main():
    # Folder yaratish
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
        
    # Flaskni alohida oqimda ishga tushirish
    threading.Thread(target=run_flask, daemon=True).start()
    
    # Botni ishga tushirish
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
