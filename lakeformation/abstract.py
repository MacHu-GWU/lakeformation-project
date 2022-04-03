# -*- coding: utf-8 -*-

import abc


class HashableAbc(abc.ABC):
    @property
    @abc.abstractmethod
    def id(self) -> str:
        raise NotImplementedError

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other: 'HashableAbc'):
        return self.id == other.id

    def __ne__(self, other: 'HashableAbc'):
        return not self.__eq__(other)


class SerializableAbc(abc.ABC):
    @abc.abstractmethod
    def serialize(self) -> dict:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def deserialize(cls, data: dict) -> 'SerializableAbc':
        raise NotImplementedError


class RenderableAbc(abc.ABC):
    @property
    @abc.abstractmethod
    def var_name(self):
        """

        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def __repr__(self):
        raise NotImplementedError

    def render(self):
        return f"{self.var_name} = {self.__repr__()}"
