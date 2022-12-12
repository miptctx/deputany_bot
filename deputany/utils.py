from deputany.settings import getConfig
from deputany.strings import *


def duma_req_url(params={}):
  params.update({str_app_token: getConfig(str_duma, str_app_key)})
  query = '&'.join([f"{params[key]}" for key in params.keys()])
  return f"{getConfig(str_duma, str_url)}/{getConfig(str_duma, str_own_key)}?{query}"
