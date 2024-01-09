import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config_data.config import Config, load_config
from handlers import user_handlers, other_handlers
from keyboards.main_menu import set_main_menu


logger = logging.getLogger(__name__)


config: Config = load_config()
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


async def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(filename)s:%(lineno)d #%(levelname)-8s '
                        '[%(asctime)s] - %(name)s - %(message)s')
    logger.info('Bot started successfully')
    
    await set_main_menu(bot)
    
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
    
if __name__ == '__main__':
    asyncio.run(main())