from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message
from states.states import DownloadState


router = Router()


@router.message(StateFilter(default_state))
async def process_wrong_answer(message: Message, state: FSMContext):
    await message.answer('I don\'t understeand you')