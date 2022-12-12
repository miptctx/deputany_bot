import os
import signal
import asyncio
import argparse
from deputany.logger import logger, logging
from deputany.settings import setConfig, updateConfig
from deputany.app import Application
from deputany.strings import *


async def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-s", "--settings", help="Settings file location")
  parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true", default=False)

  args = parser.parse_args()

  if args.settings:
    updateConfig(args.settings)

  if args.verbose:
    logger.setLevel(logging.DEBUG)

  app = Application()

  def sigHandle(signum):
    try:
      logger.info("signal " + str(signum))
      asyncio.create_task(app.cleanup())
    except Exception as error:
      logger.exception(error)

  loop = asyncio.get_event_loop()
  loop.add_signal_handler(signal.SIGINT, sigHandle, 'SIGINT')
  loop.add_signal_handler(signal.SIGTERM, sigHandle, 'SIGTERM')

  quit(await app())
