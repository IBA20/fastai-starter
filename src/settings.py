from typing import Annotated, Literal

from pydantic import AnyUrl, Field, HttpUrl, PositiveInt, SecretStr, StringConstraints
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    host: str = Field(
        default='localhost',
        description='Имя хоста Postgres',
    )
    port: PositiveInt = 5432
    username: str = 'postgres'
    password: SecretStr = 'postgres'


class DeepSeekSettings(BaseSettings):
    base_url: HttpUrl
    model: Annotated[str, StringConstraints(min_length=1)]
    api_key: SecretStr
    max_connections: PositiveInt = 5
    connection_timeout: PositiveInt = 100


class UnsplashSettings(BaseSettings):
    base_url: HttpUrl
    api_key: SecretStr
    max_connections: PositiveInt = 5
    connection_timeout: PositiveInt = 20


class StorageSettings(BaseSettings):
    endpoint_url: AnyUrl = 'http://localhost:9000'
    bucket_name: Annotated[str, StringConstraints(min_length=1)]
    access_key: SecretStr
    secret_key: SecretStr
    max_pool_connections: PositiveInt = 50
    connect_timeout: PositiveInt = 10
    read_timeout: PositiveInt = 30


class GotenbergSettings(BaseSettings):
    base_url: HttpUrl = 'https://demo.gotenberg.dev'
    screenshot_width: PositiveInt = 1000
    screenshot_format: Literal['jpeg', 'png', 'webp'] = 'png'
    max_connections: PositiveInt = 5
    wait_delay: PositiveInt = 8
    timeout: PositiveInt = 20


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        env_nested_delimiter='__',
        env_prefix='FASTAI_',
        validate_default=True,
        extra='ignore',
    )

    database: DatabaseSettings
    debug: bool = False
    deepseek: DeepSeekSettings
    unsplash: UnsplashSettings
    storage: StorageSettings
    gotenberg: GotenbergSettings


settings = AppSettings()
