from dataclasses import dataclass
from typing import List

import yaml


@dataclass
class MQConfig:
    brokers: List[str]
    topic: str


@dataclass
class CacheConfig:
    host: str
    port: int
    password: str
    db: int


@dataclass
class Config:
    cache: CacheConfig
    mq: MQConfig


def parseConfig(filename: str) -> Config:
    with open(filename, 'r') as f:
        data = yaml.safe_load(f)
        return Config(
            CacheConfig(**data['cache']),
            MQConfig(**data['mq'])

        )
