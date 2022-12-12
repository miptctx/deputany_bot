import asyncio
from aiogram import Bot, Dispatcher, executor, types
from deputany.settings import getConfig
from deputany.strings import *


'''
class Bot:
  def __init__(self, app):
    self.app = app
    self.bot = IoBot(token=getConfig(str_bot, str_token))
    self.dsp = Dispatcher(self.bot)

    # self.dsp.register_message_handler(lambda msg: self.welcome(msg), commands=['start', 'welcome'])
    # self.dsp.register_message_handler(lambda msg: self.echo(msg))
    self.dsp.register_message_handler(self.welcome, commands=['start', 'welcome'])
    self.dsp.register_message_handler(self.echo)

  async def __call__(self):
    # loop = asyncio.get_running_loop()
    await self.dsp.start_polling()
    # await executor.start_polling(self.dsp, skip_updates=True, loop=loop)

  @staticmethod
  async def welcome(message: types.Message):
    logger.debug(f"income start message: {message}")
    await message.reply("Hello!\nSend any message to start")

  @staticmethod
  async def echo(message: types.Message):
    logger.debug(f"income message: {message}")
    await message.answer(message.text)

  async def close(self):
    # executor.stop_polling()
    # await executor.wait_closed()
    self.dsp.stop_polling()
    await self.dsp.wait_closed()
'''

def bot(app):
  bot = Bot(token=getConfig(str_bot, str_token))
  dp = Dispatcher(bot)


  @dp.message_handler(commands=['start', 'help'])
  async def send_welcome(message: types.Message):
    await message.reply("Введите ключевые слова для поиска законопроекта")


  '''
  @dp.message_handler(regexp='(^cat[s]?$|puss)')
  async def cats(message: types.Message):
    with open('data/cats.jpg', 'rb') as photo:
      await message.reply_photo(photo, caption='Cats are here 😺')
  '''

  @dp.message_handler()
  async def echo(message: types.Message):
    # await message.answer(message.text)
    await app.handleMessage(message)

  return dp
