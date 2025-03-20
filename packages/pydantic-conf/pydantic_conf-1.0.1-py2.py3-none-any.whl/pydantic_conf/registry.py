from typing import Type, TypeVar, ClassVar, Self, Unpack

from pydantic import BaseModel, ConfigDict


T = TypeVar("T")


class Registry(BaseModel):
    _REGISTRY: ClassVar[dict[str, Type[Self]]] = {}

    def __init_subclass__(cls, **kwargs: Unpack[ConfigDict]):
        super().__init_subclass__(**kwargs)

        if cls.__name__ in cls._REGISTRY and cls.model_fields:
            raise ValueError(f"Duplicate name: {cls.__name__}")

        cls._REGISTRY[cls.__name__] = cls

    @classmethod
    def get_model(cls, name: str) -> Type[Self]:
        return cls._REGISTRY[name]
