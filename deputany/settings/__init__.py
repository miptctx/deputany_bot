import json
from deputany.strings import *


configs = {
  str_bot: {
    str_token: str_deadbeaf
  },
  str_duma: {
    str_url: "http://api.duma.gov.ru/api",
    str_own_key: str_deadbeaf,
    str_app_key: str_deadbeaf
  }
}


def getConfigHelper(cfg, path, *args):
  if path in cfg:
    value = cfg[path]
    return getConfigHelper(value, *args) if len(args) > 0 else value

  return None


def getConfig(*args):
  return getConfigHelper(configs, *args) if len(args) else configs


def setConfigHelper(cfg, value, path, *args):
  cfg[path] = setConfigHelper(cfg[path], value, *args) if len(args) > 0 else value
  return cfg


def setConfig(value, *args):
  setConfigHelper(configs, value, *args)


def updateConfig(file):
  with open(file, 'r') as f:
    configs.update(json.loads(f.read()))
