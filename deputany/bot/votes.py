from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from deputany.bot.state import BotState
from deputany.logger import logger
from deputany.strings import *


def parseVotes(law, data):
  placeholder = f'Голосования по законопроекту <b>{law}</b> не найдены'
  total = int(data[str_totalCount])
  length = len(data[str_votes]) if str_votes in data else 0
  votes = data[str_votes] if length else []
  return (total, length, votes, placeholder)


async def printVote(message, text, number, law):
  logger.info(f"Vote: {text}")
  like = InlineKeyboardButton(text="👍", callback_data=f"{str_like_vote_}{number}")
  dislike = InlineKeyboardButton(text="👎", callback_data=f"{str_dislike_vote_}{number}")
  kb = InlineKeyboardMarkup().row(like, dislike)
  await message.reply(text, parse_mode=str_HTML, reply_markup=kb)


async def printVotes(transport, law, votes):
  for vote in votes:
    number = vote[str_id]
    date = vote[str_voteDate]
    subject = vote[str_subject]
    result = "❌" if vote[str_result] else "✅"
    text = f'{result} <b>{number}</b> <i>{date}</i> {subject}'
    await printVote(transport, text, number, law)


async def printVotesProgress(transport, law, length, total):
  btn = InlineKeyboardButton(text="Далее", callback_data=str_votes_next)
  kb = InlineKeyboardMarkup().add(btn)
  await transport.reply(f"\n\nПоказано <b>{length}</b> из <b>{total}</b> голосований законопроекта {law}", parse_mode=str_HTML, reply_markup=kb)


async def handle_votes(message, law, state, app):
  total, length, votes, placeholder = parseVotes(law, await app.handleVotes(law))
  logger.info(f"got {length} from {total} votes of law {law}")
  if length:
    await printVotes(message, law, votes)
    if length < total:
      await BotState.votes.set()
      await state.update_data(page=1, total=total, length=length, law=law)
      await printVotesProgress(message, law, length, total)
  else:
    await message.reply(placeholder, parse_mode=str_HTML)


async def handle_votes_next(message, state, app):
  page = -1
  curlen = 0
  law = ""
  async with state.proxy() as data:
    page = data[str_page] + 1
    curlen = data[str_length]
    total = data[str_total]
    law = data[str_law]

  tot, length, votes, placeholder = parseVotes(law, await app.handleVotes(law, page=page))
  await printVotes(message, law, votes)

  if length and (curlen + length) < total:
    length = curlen+length
    await state.update_data(page=page, length=length)
    await printVotesProgress(message, law, length, total)
  elif await state.get_state() is not None:
    await BotState.previous()
