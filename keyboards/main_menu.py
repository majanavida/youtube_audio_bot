from aiogram import Bot
from aiogram.types import BotCommand


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='start', description='Start bot'),
        BotCommand(command='help', description='Get help'),
        BotCommand(command='audio', 
                   description='Download audio from YouTube video'),
        BotCommand(command='cancel', 
                   description='Cancel download')]
    await bot.set_my_commands(main_menu_commands)