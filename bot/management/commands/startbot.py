from aiogram import Bot
from django.core.management.base import BaseCommand
import asyncio
import logging

from bot.bot import bot, dp
from bot.handlers import all_routers
from core.settings import ADMIN


class Command(BaseCommand):
    help = "Start Telegram bot using Aiogram"

    async def startup(self, bot: Bot):
        await bot.send_message(chat_id=ADMIN, text="<b>Bot ishga tushdi✅</b>")

    async def shutdown(self, bot: Bot):
        await bot.send_message(chat_id=ADMIN, text="<b>Bot ishdan toxtadi🛑</b>")

    def handle(self, *args, **kwargs):
        asyncio.run(self.start())

    async def start(self):
        for router in all_routers:
            dp.include_router(router)
        dp.startup.register(self.startup)
        dp.shutdown.register(self.shutdown)
        logging.basicConfig(level=logging.INFO)
        await dp.start_polling(bot)
