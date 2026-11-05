import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from core.config import settings
from database.session import async_session_maker, init_models
from bot.middlewares.db import DbSessionMiddleware
from bot.handlers.habits import router as habits_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)


async def main():
    logger.info("Підключення до бази даних...")
    await init_models()

    bot = Bot(
        token=settings.BOT_TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher()

    # Реєстрація кастомного Middleware для Dependency Injection сесії БД
    dp.update.outer_middleware(DbSessionMiddleware(session_pool=async_session_maker))

    # Підключення роутерів
    dp.include_router(habits_router)

    logger.info("Бот успішно стартував!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
