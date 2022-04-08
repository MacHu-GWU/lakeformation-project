# -*- coding: utf-8 -*-

import abc
from typing import Optional


class LFObject(abc.ABC):
    """
    LakeFormation Object
    """
    object_type: str = "LFObject"


class HashableAbc(LFObject):
    """
    Abstract class that can be hashed and support ``==`` and ``!=`` comparison.

    It has to have a ``id`` property method, returns a unique identifier in str.
    """

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


class SerializableAbc(LFObject):
    """
    Abstract class can serialize to dict and deserialize from the dict
    """

    @abc.abstractmethod
    def serialize(self) -> dict:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def deserialize(cls, data: dict) -> 'SerializableAbc':
        raise NotImplementedError


class RenderableAbc(LFObject):
    """
    Abstract class that will be rendered by Jinja2 template to create
    resource / principal declaration scripts to support playbook.
    """

    @property
    @abc.abstractmethod
    def var_name(self):
        raise NotImplementedError

    @abc.abstractmethod
    def __repr__(self):
        raise NotImplementedError

    def render(self):
        return f"{self.var_name} = {self.__repr__()}"


class PlaybookManaged(LFObject):
    """
    Abstract class that can be identified as a Playbook managed (or not) object.
    If true, then the creation / update / delete will be managed by playbook.
    For example, resource like database, table should not be Playbook managed,
    but LF Tag in the current AWS Account should be managed by Playbook.

    :param _playbook_id: internal parameter for implementation. If None,
        it means that this resource is not playbook managed. Otherwise it is.
    """
    _playbook_id: Optional[str]

    @property
    def playbook_managed(self) -> bool:
        """
        Test whether this LakeFormation object is playbook managed.
        """
        if self._playbook_id is None:
            return False
        else:
            return True
