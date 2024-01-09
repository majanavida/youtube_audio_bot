import shutil
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, FSInputFile
from pytube import YouTube
from states.states import DownloadState


router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(f'Hello, {message.from_user.username}!\n'
                         f'This is a bot with which you can download audio '
                         f'from YouTube videos.')
    
    
@router.message(Command(commands=['help']), StateFilter(default_state))
async def process_help_command(message: Message):
    await message.answer('List of commands:\n'
                         '/start - start bot\n'
                         '/help - get help\n'
                         '/audio - get audio from YouTube video\n'
                         '/cancel - cancel audio download (after using /audio)')
    
    
@router.message(Command(commands=['audio']), StateFilter(default_state))
async def process_audio_command(message: Message, state: FSMContext):
    await message.answer('Send a link to the YouTube video')
    await state.set_state(DownloadState.download)
    
    
@router.message(Command(commands=['cancel']), ~StateFilter(default_state))
async def process_cancel_command(message: Message, state: FSMContext):
    await message.answer('Action canceled')
    await state.clear()
        
        
@router.message(StateFilter(DownloadState.download,
                F.text.startswith == ('https://youtu.be/' or 
                                      'https://www.youtube.com/')))
async def process_audio_send(message: Message, state: FSMContext):
    url = message.text
    yt = YouTube(url)
    await message.answer(f'Start downloading {yt.title}')
    await download_audio(url=url, message=message)
    await state.clear()
    
    
async def download_audio(url, message):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        audio = stream.download(f'{message.chat.id}', f'{yt.title}.mp3')
        with open(f'{message.chat.id}/{yt.title}.mp3', 'rb') as audio:
            await message.answer_audio(FSInputFile(
                                    path=f'{message.chat.id}/{yt.title}.mp3'),
                                    caption='Here is your audio')
    except FileNotFoundError:
        await message.answer('Something went wrong... Try again or send '
                             'another url')
    shutil.rmtree(f'{message.chat.id}')