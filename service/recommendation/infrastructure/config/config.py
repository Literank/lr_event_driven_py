from dataclasses import dataclass
from typing import List
import yaml


@dataclass
class DBConfig:
    mongo_uri: str
    mongo_db_name: str


@dataclass
class MQConfig:
    brokers: List[str]
    topic: str
    group_id: str


@dataclass
class ApplicationConfig:
    page_size: int


@dataclass
class Config:
    app: ApplicationConfig
    db: DBConfig
    mq: MQConfig


def parseConfig(filename: str) -> Config:
    with open(filename, 'r') as f:
        data = yaml.safe_load(f)
        return Config(
            ApplicationConfig(**data['app']),
            DBConfig(**data['db']),
            MQConfig(**data['mq'])
        )
