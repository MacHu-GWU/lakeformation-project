# -*- coding: utf-8 -*-

import re
from typing import Union, Dict, Type

from .abstract import HashableAbc, RenderableAbc, SerializableAbc
from .validator import validate_attr_type

iam_arn_pattern = re.compile("^arn:aws:iam::\d{12}:(role|user|group)/.+")


def validate_iam_arn(arn: str):
    if re.match(iam_arn_pattern, arn) is None:
        raise ValueError(f"{arn!r} is not a valid IAM arn")


class Principal(HashableAbc, RenderableAbc, SerializableAbc):
    """
    Data Accessor Principal Model.
    """
    principal_type: str = None

    @classmethod
    def deserialize(cls, data: dict) -> Union[
        'IamRole', 'IamUser', 'IamGroup'
    ]:
        return _principal_type_mapper[data["principal_type"]].deserialize(data)


class Iam(Principal):
    _prefix: str = None

    def __init__(
        self,
        arn: str,
    ):
        self.arn = arn
        self.validate()

    def validate(self):
        validate_attr_type(self, "arn", self.arn, str)
        validate_iam_arn(self.arn)

    @property
    def id(self):
        return self.arn

    @property
    def var_name(self):
        return "{}_{}".format(
            self._prefix,
            self.arn.split("/", 1)[1].replace("-", "_").replace(".", "_").replace("/", "__")
        )

    def __repr__(self):
        return f'{self.__class__.__name__}(arn={self.arn!r})'

    def serialize(self):
        return dict(principal_type=self.principal_type, arn=self.arn)


class IamRole(Iam):
    principal_type: str = "IamRole"
    _prefix: str = "role"

    @classmethod
    def deserialize(cls, data: dict) -> 'IamRole':
        return cls(arn=data["arn"])


class IamUser(Iam):
    principal_type: str = "IamUser"
    _prefix: str = "user"

    @classmethod
    def deserialize(cls, data: dict) -> 'IamUser':
        return cls(arn=data["arn"])


class IamGroup(Iam):
    principal_type: str = "IamGroup"
    _prefix: str = "group"

    @classmethod
    def deserialize(cls, data: dict) -> 'IamGroup':
        return cls(arn=data["arn"])


class SamlPrincipal(Principal):
    pass


class ExternalAccountPrincipal(Principal):
    pass


_principal_type_mapper: Dict[str, Type['Principal']] = {
    "IamRole": IamRole,
    "IamUser": IamUser,
    "IamGroup": IamGroup,
}
