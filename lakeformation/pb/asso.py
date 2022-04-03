# -*- coding: utf-8 -*-

"""
Association Class
"""

from ..abstract import HashableAbc, SerializableAbc
from ..lf_tag import LfTag
from ..principal import Principal
from ..permission import Permission
from ..constant import DELIMITER


class GrantedPermission(HashableAbc, SerializableAbc):
    def __init__(
        self,
        tag: LfTag,
        principal: Principal,
        permission: Permission,
    ):
        self.tag = tag
        self.principal = principal
        self.permission = permission

    @property
    def id(self):
        return DELIMITER.join([
            self.tag.id, self.principal.id, self.permission.id,
        ])

    def serialize(self) -> dict:
        return dict(
            tag=self.tag.serialize(),
            principal=self.principal.serialize(),
            permission=self.permission.serialize(),
        )

    @classmethod
    def deserialize(cls, data: dict) -> 'PrincipalAttachment':
        return cls(
            tag=LfTag.deserialize(data["tag"]),
            principal=Principal.deserialize(data["principal"]),
            permission=Permission.deserialize(data["permission"]),
        )
