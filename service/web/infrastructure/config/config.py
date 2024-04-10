from dataclasses import dataclass
from typing import List
import yaml


@dataclass
class DBConfig:
    host: str
    port: int
    user: str
    password: str
    database: str


@dataclass
class MQConfig:
    brokers: List[str]
    topic: str


@dataclass
class ApplicationConfig:
    port: int
    page_size: int
    templates_dir: str


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
