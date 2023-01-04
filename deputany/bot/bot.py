from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from aiogram.dispatcher.filters import Regexp
from deputany.bot.state import BotState
from deputany.bot.laws import handle_laws, handle_laws_next
from deputany.bot.votes import handle_votes, handle_votes_next
from deputany.settings import getConfig
from deputany.logger import logger
from deputany.strings import *


def handleError(func):
  async def wrapper(*args, **kwargs):
    try:
      return await func(*args, **kwargs)
    except Exception as error:
      logger.exception(error)

  return wrapper


def bot(app):
  bot = Bot(token=getConfig(str_bot, str_token), timeout=10)
  dp = Dispatcher(bot, storage=MemoryStorage())

  dp.middleware.setup(LoggingMiddleware())


  @dp.message_handler(commands=['start', 'help'])
  @handleError
  async def send_welcome(message: types.Message, **kwargs):
    await message.reply('Введите ключевые слова для поиска законопроекта, например "Курение" или "Полиция"')


  @dp.callback_query_handler(Regexp(f"^{str_votes_next}$"), state=BotState.votes)
  @handleError
  async def votes_next(call: types.CallbackQuery, state: FSMContext, **kwargs):
    logger.info(f"votes_next()")
    await handle_votes_next(call.message, state, app)
    await call.answer()


  @dp.callback_query_handler(Regexp(f"^{str_vote_of_}[0-9-]+$"), state="*")
  @handleError
  async def votes(call: types.CallbackQuery, state: FSMContext, **kwargs):
    logger.info(f"votes()")
    await handle_votes(call.message, call.data.replace(str_vote_of_, ""), state, app)
    await call.answer()


  @dp.callback_query_handler(Regexp(f"^{str_like_vote_}[0-9-]+$"), state="*")
  @handleError
  async def like_vote(call: types.CallbackQuery, state: FSMContext, **kwargs):
    logger.info(f"like_vote()")
    vote = call.data.replace(str_like_vote_, "")
    text = f"✅ 👍 Вы поддержали голосование {vote}"
    await call.message.answer(text)
    await call.answer(text)


  @dp.callback_query_handler(Regexp(f"^{str_dislike_vote_}[0-9-]+$"), state="*")
  @handleError
  async def dislike_vote(call: types.CallbackQuery, state: FSMContext, **kwargs):
    logger.info(f"dislike_vote()")
    vote = call.data.replace(str_dislike_vote_, "")
    text = f"❌ 👎 Вы не поддержали голосование {vote}"
    await call.message.answer(text)
    await call.answer(text)


  @dp.callback_query_handler(Regexp(f"^{str_laws_next}$"), state=BotState.laws)
  @handleError
  async def laws_next(call: types.CallbackQuery, state: FSMContext, **kwargs):
    logger.info(f"laws_next()")
    await handle_laws_next(call.message, state, app)
    await call.answer()


  @dp.message_handler(state="*")
  @handleError
  async def laws(message: types.Message, state: FSMContext, **kwargs):
    logger.info(f"laws()")
    await handle_laws(message, state, app)


  return dp
