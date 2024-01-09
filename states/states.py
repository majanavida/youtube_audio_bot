from aiogram.fsm.state import StatesGroup, State


class DownloadState(StatesGroup):
    download = State()