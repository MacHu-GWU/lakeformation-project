# -*- coding: utf-8 -*-

"""
Association Class
"""

from ..abstract import HashableAbc, SerializableAbc
from ..resource import Resource, NonLfTagResource, Database, Table, Column, LfTag
from ..principal import Principal
from ..permission import Permission
from ..constant import DELIMITER
from ..validator import validate_attr_type


class DataLakePermission(HashableAbc, SerializableAbc):
    def __init__(
        self,
        principal: Principal,
        resource: Resource,
        permission: Permission,
    ):
        self.principal = principal
        self.resource = resource
        self.permission = permission
        self.validate()

    def validate(self):
        validate_attr_type(self, "principal", self.principal, Principal)
        validate_attr_type(self, "resource", self.resource, Resource)
        validate_attr_type(self, "permission", self.permission, Permission)

    @property
    def id(self):
        return DELIMITER.join([
            self.principal.id, self.resource.id, self.permission.id,
        ])

    def serialize(self) -> dict:
        return dict(
            principal=self.principal.serialize(),
            resource=self.resource.serialize(),
            permission=self.permission.serialize(),
        )

    @classmethod
    def deserialize(cls, data: dict) -> 'DataLakePermission':
        return cls(
            principal=Principal.deserialize(data["principal"]),
            resource=Resource.deserialize(data["resource"]),
            permission=Permission.deserialize(data["permission"]),
        )


class LfTagAttachment(HashableAbc, SerializableAbc):
    def __init__(
        self,
        resource: NonLfTagResource,
        tag: LfTag,
    ):
        self.resource = resource
        self.tag = tag
        self.validate()

    def validate(self):
        validate_attr_type(self, "resource", self.resource, NonLfTagResource)
        validate_attr_type(self, "tag", self.tag, LfTag)

    @property
    def id(self):
        return DELIMITER.join([
            self.resource.id, self.tag.id
        ])

    def serialize(self) -> dict:
        return dict(
            resource=self.resource.serialize(),
            tag=self.tag.serialize(),
        )

    @classmethod
    def deserialize(cls, data: dict) -> 'LfTagAttachment':
        return cls(
            resource=Resource.deserialize(data["resource"]),
            tag=LfTag.deserialize(data["tag"]),
        )
