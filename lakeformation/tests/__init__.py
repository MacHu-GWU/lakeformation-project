# -*- coding: utf-8 -*-

import json
from typing import List, Union

import boto3

from ..principal import (
    Principal, Iam, IamRole, IamUser, IamGroup,
    ExternalAccount,
)
from ..resource import (
    Resource, Database, Table, Column,
    DataLakeLocation, DataCellsFilter, LfTag
)
from ..permission import PermissionEnum
from ..pb.asso import DataLakePermission, LfTagAttachment

aws_account_id = "111122223333"
aws_region = "us-east-1"


class Objects:
    def __init__(self):
        self.aws_account_id = aws_account_id
        self.aws_region = aws_region

        # --- Principal
        self.iam_role_ec2_web_app = IamRole(arn=f"arn:aws:iam::{aws_account_id}:role/ec2-web-app")
        self.iam_service_role_ecs = IamRole(
            arn=f"arn:aws:iam::{aws_account_id}:role/aws-service-role/ecs.amazonaws.com/AWSServiceRoleForECS")
        self.iam_user_alice = IamUser(arn=f"arn:aws:iam::{aws_account_id}:user/alice")
        self.iam_group_admin = IamGroup(arn=f"arn:aws:iam::{aws_account_id}:group/Admin")

        self.acc1 = ExternalAccount(account_id="111111111111")
        self.acc2 = ExternalAccount(account_id="222222222222")

        self.iam_list: List[Iam] = [
            self.iam_role_ec2_web_app,
            self.iam_service_role_ecs,
            self.iam_user_alice,
            self.iam_group_admin,
        ]

        self.acc_list: List[ExternalAccount] = [
            self.acc1,
            self.acc2,
        ]

        self.principal_list: List[Principal] = self.iam_list + self.acc_list

        # --- Resource
        self.db_amz = Database(catalog_id="111122223333", region="us-east-1", name="amz")
        self.tb_amz_user = Table(name="user", database=self.db_amz)
        self.col_amz_user_id = Column(name="id", table=self.tb_amz_user)
        self.col_amz_user_email = Column(name="email", table=self.tb_amz_user)
        self.col_amz_user_password = Column(name="password", table=self.tb_amz_user)

        self.tb_amz_item = Table(name="item", database=self.db_amz)
        self.col_amz_item_id = Column(name="id", table=self.tb_amz_item)
        self.col_amz_item_name = Column(name="name", table=self.tb_amz_item)
        self.col_amz_item_price = Column(name="price", table=self.tb_amz_item)

        self.tb_amz_order = Table(name="order", database=self.db_amz)
        self.col_amz_order_id = Column(name="id", table=self.tb_amz_order)
        self.col_amz_order_buyer = Column(name="buyer", table=self.tb_amz_order)
        self.col_amz_order_created_time = Column(name="created_time", table=self.tb_amz_order)

        self.db_list: List[Database] = [
            self.db_amz,
        ]
        self.tb_list: List[Table] = [
            self.tb_amz_user,
            self.tb_amz_item,
            self.tb_amz_order,
        ]
        self.col_list: List[Column] = [
            self.col_amz_user_id,
            self.col_amz_user_email,
            self.col_amz_user_password,
            self.col_amz_item_id,
            self.col_amz_item_name,
            self.col_amz_item_price,
            self.col_amz_order_id,
            self.col_amz_order_buyer,
            self.col_amz_order_created_time,
        ]

        self.tag_admin_y = LfTag(catalog_id=self.aws_account_id, key="admin", value="y")
        self.tag_admin_n = LfTag(catalog_id=self.aws_account_id, key="admin", value="n")
        self.tag_regular_y = LfTag(catalog_id=self.aws_account_id, key="regular", value="y")
        self.tag_regular_n = LfTag(catalog_id=self.aws_account_id, key="regular", value="n")
        self.tag_limited_y = LfTag(catalog_id=self.aws_account_id, key="limited", value="y")
        self.tag_limited_n = LfTag(catalog_id=self.aws_account_id, key="limited", value="n")

        self.tag_list: List[LfTag] = [
            self.tag_admin_y,
            self.tag_admin_n,
            self.tag_regular_y,
            self.tag_regular_n,
            self.tag_limited_y,
            self.tag_limited_n,
        ]

        self.dl_loc = DataLakeLocation(
            catalog_id=self.aws_account_id,
            resource_arn=f"arn:aws:s3:::{self.aws_account_id}-{self.aws_region}-artifacts/datalake/*",
        )

        self.data_filter = DataCellsFilter(
            filter_name="no-user-password",
            catalog_id=self.aws_account_id,
            database_name=self.db_amz.name,
            table_name=self.tb_amz_user.name,
            column_level_access=DataCellsFilter.ColumnLevelAccessEnum.exclude,
            exclude_columns=[self.col_amz_user_password.name, ]
        )

        self.resource_list: List[Resource] = \
            self.db_list \
            + self.tb_list \
            + self.col_list \
            + self.tag_list \
            + [self.dl_loc, self.data_filter]

        # --- DataLake Permission
        self.dl_permission_iam_user_alice_tag_admin_y = DataLakePermission(
            principal=self.iam_user_alice,
            resource=self.tag_admin_y,
            permission=PermissionEnum.SuperDatabase.value,
        )

        # --- LfTagAttachment
        self.attachment_db_amz_tag_admin_y = LfTagAttachment(
            resource=self.db_amz,
            tag=self.tag_admin_y,
        )
        self.attachment_col_amz_user_password_tag_regular_n = LfTagAttachment(
            resource=self.col_amz_user_password,
            tag=self.tag_regular_n,
        )


class AWS:
    def __init__(self):
        self.boto_ses = boto3.session.Session()
        self.aws_account_id = self.boto_ses.client("sts").get_caller_identity()["Account"]
        self.aws_region = self.boto_ses.region_name
        self.iam_client = self.boto_ses.client("iam")
        self.glue_client = self.boto_ses.client("glue")
        self.s3_client = self.boto_ses.client("s3")
        self.lf_client = self.boto_ses.client("lakeformation")

        self.iam_role = IamRole(arn=f"arn:aws:iam::{self.aws_account_id}:role/lakeformation-unittest")
        self.iam_user = IamGroup(arn=f"arn:aws:iam::{self.aws_account_id}:user/lakeformation-unittest")
        self.iam_group = IamGroup(arn=f"arn:aws:iam::{self.aws_account_id}:group/lakeformation-unittest")

        self.db = Database(
            catalog_id=self.aws_account_id,
            region=self.aws_region,
            name="lakeformation_unittest",
        )
        self.tb = Table(name="users", database=self.db)

        self.s3_bucket_name = f"{self.aws_account_id}-{self.aws_region}-lakeformation-unittest-fake-bucket"

        self.dl_loc = DataLakeLocation(
            catalog_id=self.aws_account_id,
            resource_arn=f"arn:aws:s3:::{self.s3_bucket_name}"
        )
        self.data_filter = DataCellsFilter(
            filter_name="lakeformation_unittest",
            catalog_id=self.aws_account_id,
            database_name=self.db.name,
            table_name=self.tb.name,
            column_level_access=DataCellsFilter.ColumnLevelAccessEnum.all,
        )

        self.tag = LfTag(catalog_id=self.aws_account_id, key="lf-unittest", value="y")

    def create_all(self):
        """
        Create Order:

        1. IAM
        2. S3 Bucket
        3. Glue Database / Table
        4. Data Lake Location
        5. Data Cell Filter
        6. LF Tag
        7. LF Tag Attachment
        8. Data Lake Permission
        """
        try:
            self.iam_client.create_role(
                RoleName=self.iam_role.name,
                AssumeRolePolicyDocument=json.dumps({
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {
                                "Service": [
                                    "ec2.amazonaws.com"
                                ]
                            },
                            "Action": [
                                "sts:AssumeRole"
                            ]
                        }
                    ]
                })
            )
        except Exception as e:
            if "already exists" not in str(e):
                raise e

        try:
            self.iam_client.create_user(
                UserName=self.iam_user.name,
            )
        except Exception as e:
            if "already exists" not in str(e):
                raise e

        try:
            self.iam_client.create_group(
                GroupName=self.iam_group.name
            )
        except Exception as e:
            if "already exists" not in str(e):
                raise e

        self.s3_client.create_bucket(
            Bucket=self.s3_bucket_name
        )

        try:
            self.glue_client.create_database(
                CatalogId=self.db.catalog_id,
                DatabaseInput=dict(
                    Name=self.db.name,
                )
            )
        except Exception as e:
            if "already exists" not in str(e):
                raise e

        try:
            self.glue_client.create_table(
                CatalogId=self.tb.catalog_id,
                DatabaseName=self.tb.database.name,
                TableInput=dict(
                    Name=self.tb.name,
                    StorageDescriptor=dict(
                        Columns=[
                            dict(Name="id", Type="integer"),
                            dict(Name="name", Type="string"),
                        ]
                    )
                )
            )
        except Exception as e:
            if "already exists" not in str(e):
                raise e

        try:
            self.lf_client.register_resource(
                ResourceArn=self.dl_loc.resource_arn,
                UseServiceLinkedRole=True,
            )
        except Exception as e:
            if "already registered" not in str(e):
                raise e

        try:
            self.lf_client.create_data_cells_filter(
                TableData=dict(
                    TableCatalogId=self.data_filter.catalog_id,
                    DatabaseName=self.data_filter.database_name,
                    TableName=self.data_filter.table_name,
                    Name=self.data_filter.filter_name,
                    RowFilter=dict(
                        FilterExpression="name='alice'"
                    ),
                    ColumnNames=[],
                    ColumnWildcard=dict(
                        ExcludedColumnNames=[]
                    )
                )
            )
        except Exception as e:
            if "already exists" not in str(e):
                raise e

        try:
            self.lf_client.create_lf_tag(
                CatalogId=self.tag.catalog_id,
                TagKey=self.tag.key,
                TagValues=[self.tag.value, ]
            )
        except Exception as e:
            if "already exists" not in str(e):
                raise e

        self.lf_client.add_lf_tags_to_resource(
            CatalogId=self.aws_account_id,
            Resource=dict(
                Database=dict(
                    CatalogId=self.db.catalog_id,
                    Name=self.db.name,
                ),
            ),
            LFTags=[
                dict(
                    CatalogId=self.tag.catalog_id,
                    TagKey=self.tag.key,
                    TagValues=[self.tag.value, ]
                )
            ],
        )

        self.lf_client.batch_grant_permissions(
            CatalogId=self.aws_account_id,
            Entries=[
                dict(
                    Id="p1",
                    Principal=dict(
                        DataLakePrincipalIdentifier=self.iam_user.arn,
                    ),
                    Resource=dict(
                        LFTagPolicy=dict(
                            CatalogId=self.tag.catalog_id,
                            ResourceType=PermissionEnum.DescribeDatabase.value.resource_type,
                            Expression=[
                                dict(
                                    TagKey=self.tag.key,
                                    TagValues=[self.tag.value,],
                                )
                            ],
                        )
                    ),
                    Permissions=[
                        PermissionEnum.DescribeDatabase.value.permission,
                    ],
                    PermissionsWithGrantOption=[],
                )
            ],
        )

    def delete_all(self):
        """
        Delete order:

        1. IAM
        2. Data Lake Location
        3. Data Cell Filter
        4. LF Tag Attachment
        5. Data Lake Permission
        6. Glue Database / Table
        7. S3 Bucket
        8. LF Tag
        """
        try:
            self.iam_client.delete_role(
                RoleName=self.iam_role.name
            )
        except Exception as e:
            if "cannot be found" not in str(e):
                raise e

        try:
            self.iam_client.delete_user(
                UserName=self.iam_user.name
            )
        except Exception as e:
            if "cannot be found" not in str(e):
                raise e

        try:
            self.iam_client.delete_group(
                GroupName=self.iam_group.name
            )
        except Exception as e:
            if "cannot be found" not in str(e):
                raise e

        try:
            self.lf_client.deregister_resource(
                ResourceArn=self.dl_loc.resource_arn,
            )
        except Exception as e:
            if "Entity not found" not in str(e):
                raise e

        try:
            self.lf_client.delete_data_cells_filter(
                TableCatalogId=self.data_filter.catalog_id,
                DatabaseName=self.data_filter.database_name,
                TableName=self.data_filter.table_name,
                Name=self.data_filter.filter_name,
            )
        except Exception as e:
            if "Resource does not exist" not in str(e):
                raise e

        try:
            self.lf_client.remove_lf_tags_from_resource(
                CatalogId=self.aws_account_id,
                Resource=dict(
                    Database=dict(
                        CatalogId=self.db.catalog_id,
                        Name=self.db.name,
                    ),
                ),
                LFTags=[
                    dict(
                        CatalogId=self.tag.catalog_id,
                        TagKey=self.tag.key,
                        TagValues=[self.tag.value, ]
                    )
                ],
            )
        except Exception as e:
            if "not found" not in str(e):
                raise e

        self.lf_client.batch_revoke_permissions(
            CatalogId=self.aws_account_id,
            Entries=[
                dict(
                    Id="p1",
                    Principal=dict(
                        DataLakePrincipalIdentifier=self.iam_user.arn,
                    ),
                    Resource=dict(
                        LFTagPolicy=dict(
                            CatalogId=self.tag.catalog_id,
                            ResourceType=PermissionEnum.DescribeDatabase.value.resource_type,
                            Expression=[
                                dict(
                                    TagKey=self.tag.key,
                                    TagValues=[self.tag.value,],
                                )
                            ],
                        )
                    ),
                    Permissions=[
                        PermissionEnum.DescribeDatabase.value.permission,
                    ],
                    PermissionsWithGrantOption=[],
                )
            ],
        )

        try:
            self.glue_client.delete_table(
                CatalogId=self.tb.catalog_id,
                DatabaseName=self.db.name,
                Name=self.tb.name,
            )
        except Exception as e:
            if "not found" not in str(e):
                raise e

        try:
            self.glue_client.delete_database(
                CatalogId=self.db.catalog_id,
                Name=self.db.name,
            )
        except Exception as e:
            if "not found" not in str(e):
                raise e

        try:
            self.s3_client.delete_bucket(
                Bucket=self.s3_bucket_name
            )
        except Exception as e:
            if "The specified bucket does not exist" not in str(e):
                raise e

        try:
            self.lf_client.delete_lf_tag(
                CatalogId=self.tag.catalog_id,
                TagKey=self.tag.key
            )
        except Exception as e:
            if "Tag key does not exist" not in str(e):
                raise e
