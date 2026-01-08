from pydantic import Field, PositiveInt, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    host: str = Field(
        default='localhost',
        description='Имя хоста Postgres',  # Четкое пояснение
    )
    port: int = 5432
    username: str = 'postgres'
    password: SecretStr = 'postgres'


class DeepSeekSettings(BaseSettings):
    base_url: str
    model: str
    api_key: SecretStr
    max_connections: PositiveInt = 5
    connection_timeout: int = 100


class UnsplashSettings(BaseSettings):
    base_url: str
    api_key: SecretStr
    max_connections: PositiveInt = 5
    connection_timeout: int = 20


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


settings = AppSettings()
