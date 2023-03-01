from pydantic import BaseSettings
from functools import lru_cache
from sqlalchemy import engine


class DatabaseSettings(BaseSettings):
    dialect: str = None
    driver: str = None
    host: str = None
    port: int = None
    name: str = None
    username: str = None
    password: str = None

    @property
    def driver_name(self) -> str:
        if self.driver:
            return f"{self.dialect}+{self.driver}"
        else:
            return f"{self.dialect}"

    @property
    def url(self) -> engine.URL:
        return engine.URL.create(
            self.driver_name,
            self.username,
            self.password,
            self.host,
            self.port,
            self.name,
        )

    class Config:
        env_file = ".env"
        env_prefix = "database_"


class Settings(BaseSettings):
    database = DatabaseSettings()

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
