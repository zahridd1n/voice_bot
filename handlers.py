# handlers.py
from aiogram import types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from text_to_speech import text_to_speech, speech_to_text
import os


async def start_handler(message: types.Message):
    await message.answer("Salom! Matn yuboring, men uni ovozga aylantirib yuboraman 🎙️")


async def tts_handler(message: types.Message):
    try:
        audio_path = text_to_speech(message.text, message.from_user.id, message.message_id)
        await message.answer_voice(voice=types.FSInputFile(audio_path))
        os.remove(audio_path)
    except Exception as e:
        await message.answer(f"❌ Xatolik: {str(e)}")


async def handle_voice_message(message: types.Message):
    try:
        voice = message.voice
        file_info = await message.bot.get_file(voice.file_id)
        file_path = file_info.file_path
        downloaded_file = await message.bot.download_file(file_path)

        # Saqlaymiz
        ogg_file_name = f"voice_{message.from_user.id}_{message.message_id}.ogg"
        with open(ogg_file_name, 'wb') as f:
            f.write(downloaded_file.read())

        # Matnga aylantiramiz
        text = speech_to_text(ogg_file_name)

        # Natijani foydalanuvchiga yuboramiz
        await message.answer(f"🗣 Ovozdan aniqlangan matn:\n<b>{text}</b>", parse_mode=ParseMode.HTML)

        # Tozalash
        os.remove(ogg_file_name)

    except Exception as e:
        await message.answer(f"❌ Ovozli xabarda xatolik: {str(e)}")
