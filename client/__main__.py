import yaml
from app_client import Application
from argparse import ArgumentParser
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

app = Application(host, port, buffersize)
app.bind()
app.start()
