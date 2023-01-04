from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from deputany.bot.state import BotState
from deputany.logger import logger
from deputany.strings import *


def parseLaws(data):
  total = int(data[str_count])
  length = len(data[str_laws]) if str_laws in data else 0
  laws = data[str_laws] if length else []
  placeholder = 'Законопроекты под данному запросу не найдены'
  return (total, length, laws, placeholder)


async def printLaw(message, text, number):
  btn = InlineKeyboardButton(text="Голосования", callback_data=f"{str_vote_of_}{number}")
  kb = InlineKeyboardMarkup().add(btn)
  await message.reply(text, parse_mode=str_HTML, reply_markup=kb)


async def printLaws(transport, laws):
  for law in laws:
    number = law[str_number]
    text = f'<b>{number}</b> {law[str_name]}'
    await printLaw(transport, text, number)


async def printLawStatus(transport, total, length):
  btn = InlineKeyboardButton(text="Далее", callback_data=str_laws_next)
  kb = InlineKeyboardMarkup().add(btn)
  await transport.reply(f"\n\nПоказано <b>{length}</b> из <b>{total}</b>", parse_mode=str_HTML, reply_markup=kb)


async def handle_laws(message, state, app):
  total, length, laws, placeholder = parseLaws(await app.handleLaws(message.text))
  if length:
    logger.info(f'found {total} laws by "{message.text}" keyword')

    await printLaws(message, laws)

    if length < total:
      await BotState.laws.set()
      await state.update_data(page=1, total=total, length=length, law=message.text)
      await printLawStatus(message, total, length)
  else:
    await message.reply(placeholder, parse_mode=str_HTML)
    if await state.get_state() is not None:
      await state.finish()


async def handle_laws_next(message, state, app):
  page = -1
  curlen = 0
  text = ""

  logger.info(f"reading state")

  async with state.proxy() as data:
    page = data[str_page] + 1
    curlen = data[str_length]
    total = data[str_total]
    text = data[str_law]

  tot, length, laws, placeholder = parseLaws(await app.handleLaws(text, page=page))

  await printLaws(message, laws)

  if length and (curlen + length) < total:
    await state.update_data(page=page, length=(curlen+length))
    await printLawStatus(message, total, curlen + length)
  elif await state.get_state() is not None:
    await state.finish()
