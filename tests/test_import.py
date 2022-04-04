# -*- coding: utf-8 -*-

import pytest


def test():
    import lakeformation as lf

    _ = lf.Principal
    _ = lf.IamRole
    _ = lf.IamUser
    _ = lf.IamGroup
    _ = lf.Permission
    _ = lf.PermissionEnum
    _ = lf.Resource
    _ = lf.Database
    _ = lf.Table
    _ = lf.Column
    _ = lf.LfTag
    _ = lf.DataLakePermission
    _ = lf.LfTagAttachment
    _ = lf.Playbook

    _ = lf.AlterDatabase
    _ = lf.AlterDatabaseGrantable
    _ = lf.AlterTable
    _ = lf.AlterTableGrantable
    _ = lf.Associate
    _ = lf.AssociateGrantable
    _ = lf.CreateDatabase
    _ = lf.CreateDatabaseGrantable
    _ = lf.CreateTable
    _ = lf.CreateTableGrantable
    _ = lf.CreateTag
    _ = lf.CreateTagGrantable
    _ = lf.DataLocationAccess
    _ = lf.DataLocationAccessGrantable
    _ = lf.Delete
    _ = lf.DeleteGrantable
    _ = lf.DescribeDatabase
    _ = lf.DescribeDatabaseGrantable
    _ = lf.DescribeTable
    _ = lf.DescribeTableGrantable
    _ = lf.DropDatabase
    _ = lf.DropDatabaseGrantable
    _ = lf.DropTable
    _ = lf.DropTableGrantable
    _ = lf.Insert
    _ = lf.InsertGrantable
    _ = lf.Select
    _ = lf.SelectGrantable
    _ = lf.SuperDatabase
    _ = lf.SuperDatabaseGrantable
    _ = lf.SuperTable
    _ = lf.SuperTableGrantable

    _ = lf.gen_resource
    _ = lf.gen_principal


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
