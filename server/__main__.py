import yaml
import logging

from app_server import Application
from argparse import ArgumentParser
from handlers import handle_default_request
from config import Config

parser = ArgumentParser()

parser.add_argument(
    '-s', '--settings', type=str,
    required=False, help='Settings file path'
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

app = Application(host, port, buffersize, handle_default_request)
app.bind()
app.start()
