import asyncio
import logging

from aiogram import Bot, Dispatcher,F

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command  # Import the Command filter

from config import BOT_TOKEN
from handlers import start_handler, tts_handler, handle_voice_message

# Logging
logging.basicConfig(level=logging.INFO)

# Bot va dispatcher
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

# Register Handlers
dp.message.register(start_handler, Command("start"))  # Use Command filter
dp.message.register(tts_handler)
dp.message.register(handle_voice_message, F.voice)

# Botni ishga tushirish
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
