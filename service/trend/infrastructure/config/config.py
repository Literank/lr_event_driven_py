from dataclasses import dataclass

import yaml


@dataclass
class CacheConfig:
    host: str
    port: int
    password: str
    db: int


@dataclass
class Config:
    cache: CacheConfig


def parseConfig(filename: str) -> Config:
    with open(filename, 'r') as f:
        data = yaml.safe_load(f)
        return Config(
            CacheConfig(**data['cache'])
        )
