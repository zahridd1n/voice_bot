import asyncio
from aiogram import Bot
from config import BOT_TOKEN

async def delete_webhook():
    bot = Bot(token=BOT_TOKEN)
    await bot.delete_webhook(drop_pending_updates=True)
    print("Webhook deleted")

if __name__ == "__main__":
    asyncio.run(delete_webhook())
