from setuptools import setup, find_packages

setup(
  name='Deputany bot',
  version='1.0.0',
  description='The telegram bot to find more appropriate deputy',
  author='Illia Rohozhkin',
  author_email='illia.rogozhkin@gmail.com',
  url='https://github.com/systemmind/deputany_bot',
  install_requires=['aiogram==2.23.1'],
  packages=[
    'deputany', 'deputany.settings'
  ],
  package_data={'deputany': ['cfg/logging.conf']},
  scripts=['deputany/deputany-bot']
)
