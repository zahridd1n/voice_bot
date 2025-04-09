# bot.py
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
import os


from text_to_speech import text_to_speech,speech_to_text
from config import API_TOKEN

# Logging
logging.basicConfig(level=logging.INFO)

# Bot va dispatcher
bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())

# /start komandasi
@dp.message(F.text == "/start")
async def start_handler(message: types.Message):
    await message.answer("Salom! Matn yuboring, men uni ovozga aylantirib yuboraman 🎙️")

# Matnni qabul qilish va ovozga aylantirish
@dp.message(F.text)
async def tts_handler(message: types.Message):
    try:
        audio_path = text_to_speech(message.text, message.from_user.id, message.message_id)
        await message.answer_voice(voice=types.FSInputFile(audio_path))
        os.remove(audio_path)  # Fayl yuborilgandan keyin o‘chiriladi
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {str(e)}")


@dp.message(F.voice)
async def stt_handler(message: types.Message):
    try:
        # Ovozli xabarni yuklab olish
        file_info = await bot.get_file(message.voice.file_id)
        file_path = file_info.file_path
        downloaded_file = await bot.download_file(file_path)

        user_audio_path = f"voice_{message.from_user.id}_{message.message_id}.wav"
        with open(user_audio_path, "wb") as new_file:
            new_file.write(downloaded_file.read())

        # STT funksiyasiga uzatish
        text = speech_to_text(user_audio_path)

        await message.answer(f"📄 Aniqlangan matn:\n<code>{text}</code>")
        os.remove(user_audio_path)

    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {str(e)}")


# Botni ishga tushirish
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
