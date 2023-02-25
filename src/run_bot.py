import time
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from pydantic import BaseSettings
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from revChatGPT.V1 import Chatbot
import logging

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    bot_token: str
    openai_email: str
    openai_password: str
    openai_paid: bool = True

    class Config:
        env_prefix = 'SETTINGS_'


settings = Settings()

bot = Bot(token=settings.bot_token, validate_token=False)
dp = Dispatcher(bot)

FORGET_COMMAND = '/forget'


chatbot = Chatbot(config={
    "email": settings.openai_email, "password": settings.openai_password, "paid": settings.openai_paid
})


def ask_chatbot_stream(chatbot: Chatbot, prompt: str, sleep: int = 5) -> str:
    try:
        chatbot.reset_chat()
        return list(chatbot.ask(prompt=prompt))[-1]['message']
    except Exception as e:
        logger.info(f'Could not ask chatbot {e}, sleeping for {sleep} seconds')
        time.sleep(sleep)
        return ask_chatbot_stream(chatbot=chatbot, prompt=prompt, sleep=sleep + 30)


forget_button = KeyboardButton(FORGET_COMMAND)
keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(forget_button)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    welcome_message = 'Hi👋'
    await message.answer(welcome_message)


@dp.message_handler(content_types=['text'])
async def respond(message: types.Message):
    response = ask_chatbot_stream(chatbot=chatbot, prompt=message.text)
    await message.reply(response, reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dp)
