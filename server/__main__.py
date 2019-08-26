import os
import yaml
import logging

from app_server import Application
from argparse import ArgumentParser
from handlers import handle_default_request
from config import Config
from database import Base, engine
from settings import INSTALLED_MODULES, BASE_DIR

parser = ArgumentParser()

parser.add_argument(
    '-s', '--settings', type=str,
    required=False, help='Settings file path'
)

parser.add_argument(
    '-m', '--migrate', action='store_true',
)

args = parser.parse_args()

if args.settings:
    with open(args.settings) as file:
        settings = yaml.load(file, Loader=yaml.Loader)
        conf = Config(settings['host'], settings['port'], 1024)
else:
    conf = Config

host, port, buffersize = conf.host, conf.port, conf.buffersize
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('server_main.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
if args.migrate:
    module_name_list = [f'{item}.models' for item in INSTALLED_MODULES]
    module_path_list = (os.path.join(BASE_DIR, item, 'models.py') for item in INSTALLED_MODULES)
    for index, path in enumerate(module_path_list):
        if os.path.exists(path):
            __import__(module_name_list[index])
    Base.metadata.create_all()
else:
    with Application(host, port, buffersize, handle_default_request) as app:
        app.bind()
        app.start()
