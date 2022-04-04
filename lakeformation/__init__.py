# -*- coding: utf-8 -*-

"""
Package Description.
"""

from ._version import __version__

__short_description__ = "Data Access Control as Code (DACAC) Framework based on AWS LakeFormation"
__license__ = "MIT"
__author__ = "Sanhe Hu"
__author_email__ = "husanhe@gmail.com"
__github_username__ = "MacHu-GWU"

try:
    from .principal import (
        Principal, IamRole, IamUser, IamGroup,
    )
    from .permission import Permission, PermissionEnum
    from .resource import (
        Resource,
        Database, Table, Column, LfTag
    )
    from .pb import (
        DataLakePermission, LfTagAttachment,
        Playbook,
    )

    AlterDatabase: Permission = PermissionEnum.AlterDatabase.value
    AlterDatabaseGrantable: Permission = PermissionEnum.AlterDatabaseGrantable.value
    AlterTable: Permission = PermissionEnum.AlterTable.value
    AlterTableGrantable: Permission = PermissionEnum.AlterTableGrantable.value
    Associate: Permission = PermissionEnum.Associate.value
    AssociateGrantable: Permission = PermissionEnum.AssociateGrantable.value
    CreateDatabase: Permission = PermissionEnum.CreateDatabase.value
    CreateDatabaseGrantable: Permission = PermissionEnum.CreateDatabaseGrantable.value
    CreateTable: Permission = PermissionEnum.CreateTable.value
    CreateTableGrantable: Permission = PermissionEnum.CreateTableGrantable.value
    CreateTag: Permission = PermissionEnum.CreateTag.value
    CreateTagGrantable: Permission = PermissionEnum.CreateTagGrantable.value
    DataLocationAccess: Permission = PermissionEnum.DataLocationAccess.value
    DataLocationAccessGrantable: Permission = PermissionEnum.DataLocationAccessGrantable.value
    Delete: Permission = PermissionEnum.Delete.value
    DeleteGrantable: Permission = PermissionEnum.DeleteGrantable.value
    DescribeDatabase: Permission = PermissionEnum.DescribeDatabase.value
    DescribeDatabaseGrantable: Permission = PermissionEnum.DescribeDatabaseGrantable.value
    DescribeTable: Permission = PermissionEnum.DescribeTable.value
    DescribeTableGrantable: Permission = PermissionEnum.DescribeTableGrantable.value
    DropDatabase: Permission = PermissionEnum.DropDatabase.value
    DropDatabaseGrantable: Permission = PermissionEnum.DropDatabaseGrantable.value
    DropTable: Permission = PermissionEnum.DropTable.value
    DropTableGrantable: Permission = PermissionEnum.DropTableGrantable.value
    Insert: Permission = PermissionEnum.Insert.value
    InsertGrantable: Permission = PermissionEnum.InsertGrantable.value
    Select: Permission = PermissionEnum.Select.value
    SelectGrantable: Permission = PermissionEnum.SelectGrantable.value
    SuperDatabase: Permission = PermissionEnum.SuperDatabase.value
    SuperDatabaseGrantable: Permission = PermissionEnum.SuperDatabaseGrantable.value
    SuperTable: Permission = PermissionEnum.SuperTable.value
    SuperTableGrantable: Permission = PermissionEnum.SuperTableGrantable.value

    from .gen_code import gen_resource, gen_principal
except ImportError:  # pragma: no cover
    pass
