from aiogram.dispatcher.filters.state import State, StatesGroup

class BotState(StatesGroup):
  laws = State()
  votes = State()
