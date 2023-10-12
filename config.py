from environs import Env
from aiogram import Bot, Dispatcher

env = Env()
env.read_env()

bot_token = env('BOT_TOKEN').replace('"', '')
ykassa = env('YKASSA')

bot: Bot = Bot(token=bot_token)
dp: Dispatcher = Dispatcher()
