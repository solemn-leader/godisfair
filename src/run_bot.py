import logging
import time

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from pydantic import BaseSettings
from revChatGPT.V1 import Chatbot

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Settings(BaseSettings):
    bot_token: str
    openai_access_token: str
    openai_paid: bool = True

    class Config:
        env_prefix = 'SETTINGS_'


settings = Settings()

bot = Bot(token=settings.bot_token, validate_token=False)
dp = Dispatcher(bot)

FORGET_COMMAND = 'forget'

chatbot = Chatbot(config={'access_token': settings.openai_access_token, 'paid': settings.openai_paid})


def ask_chatbot_stream(chatbot: Chatbot, prompt: str, sleep: int = 5) -> str:
    try:
        return list(chatbot.ask(prompt=prompt))[-1]['message']
    except Exception as e:
        logger.info(f'Could not ask chatbot {e}, sleeping for {sleep} seconds')
        time.sleep(sleep)
        return ask_chatbot_stream(chatbot=chatbot, prompt=prompt, sleep=sleep + 5)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    welcome_message = 'Hi👋'
    await message.answer(welcome_message)


@dp.message_handler(commands=[FORGET_COMMAND])
async def send_welcome(message: types.Message):
    chatbot.reset_chat()
    logger.info('Starting new chat with user %s', message.from_user.full_name)
    await message.answer("Let's to start over again.")


@dp.message_handler(content_types=['text'])
async def respond(message: types.Message):
    text = message.text
    logger.info('Got message %s from user %s', text, message.from_user.full_name)
    response = ask_chatbot_stream(chatbot=chatbot, prompt=text)
    logger.info('Responding with %s', response)
    await message.answer(response, parse_mode='Markdown')


if __name__ == '__main__':
    logger.info('Start polling')
    executor.start_polling(dp)
