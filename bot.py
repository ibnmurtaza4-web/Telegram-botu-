import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import yt_dlp
import os

BOT_TOKEN = "BURAYA_YENI_TOKEN_YAZ"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "🤖 Salam! Mən video yükləyici botam.\n\n"
        "🎬 Video\n🎵 MP3 audio\n\n"
        "Link göndər 👇"
    )

@dp.message()
async def download_video(message: types.Message):
    url = message.text

    if not url.startswith("http"):
        await message.answer("❌ Zəhmət olmasa düzgün link göndər.")
        return

    await message.answer("⏳ Yüklənir...")

    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'video.%(ext)s'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info)

        file_size = os.path.getsize(file_name)

        # 50MB limit
        if file_size > 50 * 1024 * 1024:
            await message.answer("⚠️ Video çox böyükdür (50MB+).")
            os.remove(file_name)
            return

        await message.answer_document(open(file_name, 'rb'))

        os.remove(file_name)

    except Exception as e:
        await message.answer("❌ Yükləmə alınmadı.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
