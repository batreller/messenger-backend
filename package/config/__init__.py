from pathlib import Path

from package.config.Config import ConfigHandler

# TODO: Different configs for drop and dev setups
config_path = Path('./config/dev.json')
print(config_path.absolute())
handler = ConfigHandler(config_path)

config = handler.load()
