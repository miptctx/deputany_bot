import logging
import logging.config
import pkg_resources

cfgFile = pkg_resources.resource_filename(__name__, "cfg/logging.conf")
if cfgFile:
  logging.config.fileConfig(cfgFile)


logger = logging.getLogger('deputany')
