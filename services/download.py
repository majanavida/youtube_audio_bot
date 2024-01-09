from pytube import YouTube


async def download_audio(url, message):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    stream.download(f'{message.chat.id}', f'{yt.title}')