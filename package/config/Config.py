import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel
from pydantic.tools import parse_obj_as


class JwtConfig(BaseModel):
    expiry_time_minutes: int
    algorithm: Literal['HS256', 'HS384', 'HS512']
    secret: str


class DbConfig(BaseModel):
    connection_string: str


class AddressConfig(BaseModel):
    host: str
    port: int


class Config(BaseModel):
    jwt: JwtConfig
    db: DbConfig
    address: AddressConfig


class ConfigHandler:
    def __init__(
            self,
            config_path: Path
    ) -> None:
        self.config_path = config_path

        if not self.config_path:
            raise Exception(f"Config file at {self.config_path.absolute()} doesn't exist")

    def load(self) -> Config:
        with open(self.config_path, mode='r') as handle:
            contents = handle.read()
            config = parse_obj_as(Config, json.loads(contents))

            return config
