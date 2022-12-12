import asyncio
import requests
from deputany.logger import logger
from deputany.bot import bot
from deputany.utils import duma_req_url


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
      await self.dispatcher.start_polling()
    except asyncio.CancelledError as error:
      pass
    except BaseException as error:
      self.exitCode = -1
      logger.error(error)
    finally:
      logger.debug('application finished, exit')

  async def cleanup(self):
    logger.debug("app cleaning up")

    if self.dispatcher:
      logger.debug("bot task cancelling")
      self.dispatcher.stop_polling()
      await self.dispatcher.wait_closed()
      logger.debug("bot finished")

  async def handleMessage(self, message):
    r = requests.get(url=duma_req_url({str_name: message.text}))
    resp = r.json()
    answer = 'Законопроекты под данному запросу не найдены'
    if resp[str_count]:
      answer = "\n\n".join([f"/{obj[str_id]}: {obj[str_name]}" for obj in resp[str_laws]])

    message.answer(resp)
