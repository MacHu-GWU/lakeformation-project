# -*- coding: utf-8 -*-

import enum

import attr
from attrs_mate import AttrsClass

from .abstract import HashableAbc, SerializableAbc


@attr.define
class Permission(HashableAbc, SerializableAbc):
    """
    Data Permission Model.
    """
    identifier: str = AttrsClass.ib_str(nullable=False)
    resource_type: str = AttrsClass.ib_str(nullable=False, hash=False)
    permission: str = AttrsClass.ib_str(nullable=False, hash=False)
    grantable: str = AttrsClass.ib_bool(nullable=False, hash=False)

    @property
    def id(self):
        return self.identifier

    def __repr__(self):
        return f'{self.__class__.__name__}(identifier="{self.identifier}", resource_type="{self.resource_type}", permission="{self.permission}", grantable={self.grantable})'

    def serialize(self) -> dict:
        return dict(
            identifier=self.identifier,
            resource_type=self.resource_type,
            permission=self.permission,
            grantable=self.grantable,
        )

    @classmethod
    def deserialize(cls, data: dict) -> 'Permission':
        return Permission(
            identifier=data["identifier"],
            resource_type=data["resource_type"],
            permission=data["permission"],
            grantable=data["grantable"],
        )


class PermissionEnum(enum.Enum):
    """
    Reference:

    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.batch_grant_permissions
    """
    CreateDatabase = Permission(
        identifier="CreateDatabase",
        resource_type="DATABASE",
        permission="CREATE_DATABASE",
        grantable=False,
    )

    CreateDatabaseGrantable = Permission(
        identifier="CreateDatabaseGrantable",
        resource_type="DATABASE",
        permission="CREATE_DATABASE",
        grantable=True,
    )

    AlterDatabase = Permission(
        identifier="AlterDatabase",
        resource_type="DATABASE",
        permission="ALTER",
        grantable=False,
    )

    AlterDatabaseGrantable = Permission(
        identifier="AlterDatabaseGrantable",
        resource_type="DATABASE",
        permission="ALTER",
        grantable=True,
    )

    DropDatabase = Permission(
        identifier="DropDatabase",
        resource_type="DATABASE",
        permission="DROP",
        grantable=False,
    )

    DropDatabaseGrantable = Permission(
        identifier="DropDatabaseGrantable",
        resource_type="DATABASE",
        permission="DROP",
        grantable=True,
    )

    DescribeDatabase = Permission(
        identifier="DescribeDatabase",
        resource_type="DATABASE",
        permission="DESCRIBE",
        grantable=False,
    )

    DescribeDatabaseGrantable = Permission(
        identifier="DescribeDatabaseGrantable",
        resource_type="DATABASE",
        permission="DESCRIBE",
        grantable=True,
    )

    SuperDatabase = Permission(
        identifier="SuperDatabase",
        resource_type="DATABASE",
        permission="ALL",
        grantable=False,
    )
    SuperDatabaseGrantable = Permission(
        identifier="SuperDatabaseGrantable",
        resource_type="DATABASE",
        permission="ALL",
        grantable=True,
    )

    CreateTable = Permission(
        identifier="CreateTable",
        resource_type="DATABASE",
        permission="CREATE_TABLE",
        grantable=False,
    )

    CreateTableGrantable = Permission(
        identifier="CreateTableGrantable",
        resource_type="DATABASE",
        permission="CREATE_TABLE",
        grantable=True,
    )

    Select = Permission(
        identifier="Select",
        resource_type="TABLE",
        permission="SELECT",
        grantable=False,
    )

    SelectGrantable = Permission(
        identifier="SelectGrantable",
        resource_type="TABLE",
        permission="SELECT",
        grantable=True,
    )

    Insert = Permission(
        identifier="Insert",
        resource_type="TABLE",
        permission="INSERT",
        grantable=False,
    )

    InsertGrantable = Permission(
        identifier="InsertGrantable",
        resource_type="TABLE",
        permission="INSERT",
        grantable=True,
    )

    Delete = Permission(
        identifier="Delete",
        resource_type="TABLE",
        permission="DELETE",
        grantable=False,
    )

    DeleteGrantable = Permission(
        identifier="DeleteGrantable",
        resource_type="TABLE",
        permission="DELETE",
        grantable=True,
    )

    DescribeTable = Permission(
        identifier="DescribeTable",
        resource_type="TABLE",
        permission="DESCRIBE",
        grantable=False,
    )

    DescribeTableGrantable = Permission(
        identifier="DescribeTableGrantable",
        resource_type="TABLE",
        permission="DESCRIBE",
        grantable=True,
    )

    AlterTable = Permission(
        identifier="AlterTable",
        resource_type="TABLE",
        permission="ALTER",
        grantable=False,
    )

    AlterTableGrantable = Permission(
        identifier="AlterTableGrantable",
        resource_type="TABLE",
        permission="ALTER",
        grantable=True,
    )

    DropTable = Permission(
        identifier="DropTable",
        resource_type="TABLE",
        permission="DROP",
        grantable=False,
    )

    DropTableGrantable = Permission(
        identifier="DropTableGrantable",
        resource_type="TABLE",
        permission="DROP",
        grantable=True,
    )

    SuperTable = Permission(
        identifier="SuperTable",
        resource_type="TABLE",
        permission="ALL",
        grantable=False,
    )

    SuperTableGrantable = Permission(
        identifier="SuperTableGrantable",
        resource_type="TABLE",
        permission="ALL",
        grantable=True,
    )

    DataLocationAccess = Permission(
        identifier="DataLocationAccess",
        resource_type="DataLocation",
        permission="DATA_LOCATION_ACCESS",
        grantable=True,
    )

    CreateTag = Permission(
        identifier="CreateTag",
        resource_type="Tag",
        permission="CREATE_TAG",
        grantable=True,
    )

    Associate = Permission(
        identifier="Associate",
        resource_type="Tag",
        permission="ASSOCIATE",
        grantable=True,
    )

    DataLocationAccessGrantable = Permission(
        identifier="DataLocationAccessGrantable",
        resource_type="DataLocation",
        permission="DATA_LOCATION_ACCESS",
        grantable=True,
    )

    CreateTagGrantable = Permission(
        identifier="CreateTagGrantable",
        resource_type="Tag",
        permission="CREATE_TAG",
        grantable=True,
    )

    AssociateGrantable = Permission(
        identifier="AssociateGrantable",
        resource_type="Tag",
        permission="ASSOCIATE",
        grantable=True,
    )

    @classmethod
    def _validate(cls):
        """
        Validate this enum declaration
        :return:
        """
        id_list = [permission.value.identifier for permission in cls]
        if len(id_list) != len(set(id_list)):  # pragma: no cover
            raise ValueError
