import os
from pathlib import Path

from package.config.Config import ConfigHandler

if os.environ['PYTEST_ENV']:
    config_path = Path('./config/test.json')
else:
    config_path = Path('./config/dev.json')

handler = ConfigHandler(config_path)
config = handler.load()
