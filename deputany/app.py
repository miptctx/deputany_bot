import asyncio
import requests
from deputany.logger import logger
from deputany.bot.bot import bot
from deputany.utils import duma_req_url
from deputany.strings import *


class Application:
  def __init__(self):
    self.exitCode = 0
    self.dispatcher = None

  async def __call__(self):
    await self.exec()
    return self.exitCode

  async def exec(self):
    try:
      self.dispatcher = bot(self)
      await self.dispatcher.start_polling(timeout=5, error_sleep=1)
    except asyncio.CancelledError as error:
      pass
    except BaseException as error:
      self.exitCode = -1
      logger.error(error)
    finally:
      logger.info('application finished, exit')

  async def cleanup(self):
    logger.info("app cleaning up")

    if self.dispatcher:
      logger.info("bot task cancelling")
      self.dispatcher.stop_polling()
      await self.dispatcher.wait_closed()
      logger.info("bot finished")

  async def handleLaws(self, message, **kwargs):
    url = duma_req_url('search.json', name=message, limit=10, **kwargs)
    logger.info(f"request {url}")
    r = requests.get(url=url)
    return r.json()

  async def handleVotes(self, message, **kwargs):
    url = duma_req_url('voteSearch.json', number=message, limit=10, **kwargs)
    logger.info(f"request {url}")
    r = requests.get(url=url)
    return r.json()
