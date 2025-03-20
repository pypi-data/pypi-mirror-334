import os
from abc import abstractmethod
from pathlib import Path
from typing import Self, TypeVar

from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict

from pydantic_conf.registry import Registry


T = TypeVar("T")


class AppConfig(BaseModel):
    """Application configuration."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    @classmethod
    def load(cls) -> Self:
        """Load configuration."""

        return cls._load()

    @classmethod
    @abstractmethod
    def _load(cls) -> Self:
        pass


class EnvAppConfig(AppConfig, Registry):
    """Configuration from environment variables."""

    @classmethod
    def _load(cls) -> Self:
        """Load configuration from environment variables."""

        if Path(".env").exists():
            load_dotenv()

        return cls.model_validate(os.environ)
