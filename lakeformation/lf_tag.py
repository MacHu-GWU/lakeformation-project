# -*- coding: utf-8 -*-

from typing import List, Dict, TYPE_CHECKING

from .abstract import HashableAbc, RenderableAbc, SerializableAbc
from .constant import DELIMITER
from .validator import validate_attr_type


class LfTag(HashableAbc, RenderableAbc, SerializableAbc):
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value
        self.validate()

    def validate(self):
        validate_attr_type(self, "key", self.key, str)
        validate_attr_type(self, "value", self.value, str)

    @property
    def id(self):
        return f"{self.key}{DELIMITER}{self.value}"

    @property
    def var_name(self):
        return f"lf_tag_{self.key.lower()}_{self.value.lower()}"

    def __repr__(self):
        return f"{self.__class__.__name__}(key={self.key!r}, value={self.value!r})"

    def serialize(self) -> dict:
        return dict(key=self.key, value=self.value)

    @classmethod
    def deserialize(cls, data: dict) -> 'LfTag':
        return cls(key=data["key"], value=data["value"])
