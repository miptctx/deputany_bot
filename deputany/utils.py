from deputany.settings import getConfig
from deputany.strings import *


def duma_req_url(*args, **kwargs):
  query = '&'.join([f"{str_app_token}={getConfig(str_duma, str_app_key)}"] + [f"{key}={kwargs[key]}" for key in kwargs.keys()])
  return f"{getConfig(str_duma, str_url)}/{getConfig(str_duma, str_own_key)}/{'/'.join(args)}?{query}"
