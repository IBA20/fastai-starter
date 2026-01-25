from typing import Literal

from pydantic import Field, HttpUrl, PositiveInt, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    host: str = Field(
        default='localhost',
        description='Имя хоста Postgres',
    )
    port: PositiveInt = Field(
        default=5432,
        gt=1023,
        lt=65536,
        description='Порт Postgres',
    )
    db: str = Field(
        default='postgres',
        description='Имя базы данных',
    )
    username: str = Field(
        default='postgres',
        description='Имя пользователя базы данных',
    )
    password: SecretStr = Field(
        default='postgres',
        description='Пароль пользователя базы данных',
    )

    @computed_field
    def database_url(self) -> str:
        return f'postgres://{self.username}:{self.password}{self.host}:{self.port}/{self.db}'


class DeepSeekSettings(BaseSettings):
    base_url: HttpUrl = Field(description='URL API DeepSeek')
    model: str = Field(min_length=1, description='Название модели DeepSeek')
    api_key: SecretStr = Field(min_length=1, description='АПИ-ключ API DeepSeek')
    max_connections: PositiveInt = Field(default=5, description='Максимальное число одновременных соединений')
    connection_timeout: PositiveInt = Field(default=100, description='Таймаут соединения')


class UnsplashSettings(BaseSettings):
    base_url: HttpUrl = Field(default='https://unsplash.com', description='URL API Unsplash')
    api_key: SecretStr = Field(min_length=1, description='АПИ-ключ API Unsplash')
    max_connections: PositiveInt = Field(default=5, description='Максимальное число одновременных соединений')
    connection_timeout: PositiveInt = Field(default=20, description='Таймаут соединения')


class StorageSettings(BaseSettings):
    endpoint_url: str = Field(default='http://localhost:9000', description='URL хранилища S3')
    bucket_name: str = Field(min_length=1, description='Имя бакета S3')
    access_key: SecretStr = Field(min_length=1, description='Ключ доступа хранилища S3')
    secret_key: SecretStr = Field(min_length=1, description='Секретный ключ хранилища S3')
    max_pool_connections: PositiveInt = Field(default=50, description='Максимальное число одновременных соединений')
    connect_timeout: PositiveInt = Field(default=10, description='Таймаут соединения')
    read_timeout: PositiveInt = Field(default=30, description='Таймаут чтения данных')


class GotenbergSettings(BaseSettings):
    base_url: HttpUrl = Field(default='https://demo.gotenberg.dev', description='URL API Gotenberg')
    screenshot_width: PositiveInt = Field(default=1000, description='Ширина скриншота')
    screenshot_format: Literal['jpeg', 'png', 'webp'] = Field(
        default='png',
        description='Формат скриншота (jpeg, png or webp)',
    )
    max_connections: PositiveInt = Field(default=5, description='Максимальное число одновременных соединений')
    wait_delay: PositiveInt = Field(default=8, description='Задержка перед получение м скриншота')
    timeout: PositiveInt = Field(default=20, description='Таймаут соединения + чтения')


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
