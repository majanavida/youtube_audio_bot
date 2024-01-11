import shutil
from aiogram.types import FSInputFile
from pytube import YouTube


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