# -*- coding: utf-8 -*-

from typing import Union, Optional, TYPE_CHECKING

from .abstract import HashableAbc, RenderableAbc, SerializableAbc, PlaybookManaged
from .validator import validate_attr_type
from .utils import validate_account_id, validate_iam_arn

if TYPE_CHECKING:  # pragma: no cover
    from .pb.playbook import Playbook


class Principal(HashableAbc, RenderableAbc, SerializableAbc, PlaybookManaged):
    """
    Principal Model.
    """


class Iam(Principal):
    _prefix: str = None

    def __init__(
        self,
        arn: str,
        _playbook_id: Optional[str] = None,
    ):
        self.arn = arn
        self.validate()
        self._playbook_id = _playbook_id  # IAM object is never playbook managed

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
        return dict(
            object_type=self.object_type,
            arn=self.arn,
            _playbook_id=self._playbook_id,
        )

    @property
    def name(self) -> str:
        """
        Return the IAM role / user / group base name
        """
        return self.arn.split("/")[-1]


class IamRole(Iam):
    object_type: str = "IamRole"
    _prefix: str = "role"

    @classmethod
    def deserialize(cls, data: dict) -> 'IamRole':
        return cls(
            arn=data["arn"],
            _playbook_id=data["_playbook_id"],
        )


class IamUser(Iam):
    object_type: str = "IamUser"
    _prefix: str = "user"

    @classmethod
    def deserialize(cls, data: dict) -> 'IamUser':
        return cls(
            arn=data["arn"],
            _playbook_id=data["_playbook_id"],
        )


class IamGroup(Iam):
    object_type: str = "IamGroup"
    _prefix: str = "group"

    @classmethod
    def deserialize(cls, data: dict) -> 'IamGroup':
        return cls(
            arn=data["arn"],
            _playbook_id=data["_playbook_id"],
        )


class SamlPrincipal(Principal):
    object_type = "SamlPrincipal"


class ExternalAccount(Principal):
    object_type = "ExternalAccount"

    def __init__(
        self,
        account_id: str,
        pb: 'Playbook' = None,
        _playbook_id: Optional[str] = None
    ):
        self.account_id = account_id
        self._playbook_id = _playbook_id
        self.validate()
        if pb is None:
            self._playbook_id = None
        else:
            pb.add_external_account(self)
            self._playbook_id = pb.playbook_id
        self.pb = pb

    def validate(self):
        validate_attr_type(self, "account_id", self.account_id, str)
        validate_account_id(self.account_id)

    @property
    def id(self):
        return self.account_id

    @property
    def var_name(self):
        return f"acc_{self.account_id}"

    def __repr__(self):
        return f'{self.__class__.__name__}(account_id={self.account_id!r})'

    def serialize(self):
        return dict(
            object_type=self.object_type,
            account_id=self.account_id,
            _playbook_id=self._playbook_id,
        )

    @classmethod
    def deserialize(cls, data: dict) -> 'ExternalAccount':
        return cls(
            account_id=data["account_id"],
            _playbook_id=data["_playbook_id"],
        )


_principal_type_mapper = {
    IamRole.object_type: IamRole,
    IamUser.object_type: IamUser,
    IamGroup.object_type: IamGroup,
    ExternalAccount.object_type: ExternalAccount,
}


def deserialize_principal(data: dict) -> Union[
    IamRole,
    IamUser,
    IamGroup,
    ExternalAccount,
]:
    return _principal_type_mapper[data["object_type"]].deserialize(data)
