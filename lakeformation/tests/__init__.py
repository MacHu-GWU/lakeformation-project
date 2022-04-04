# -*- coding: utf-8 -*-

from typing import List, Union
from ..principal import Iam, IamRole, IamUser, IamGroup
from ..resource import Resource, Database, Table, Column, LfTag
from ..permission import PermissionEnum
from ..pb.asso import DataLakePermission, LfTagAttachment

aws_account_id = "111122223333"
aws_region = "us-east-1"


class Objects:
    def __init__(self):
        # --- Principal
        self.iam_role_ec2_web_app = IamRole(arn=f"arn:aws:iam::{aws_account_id}:role/ec2-web-app")
        self.iam_service_role_ecs = IamRole(
            arn=f"arn:aws:iam::{aws_account_id}:role/aws-service-role/ecs.amazonaws.com/AWSServiceRoleForECS")
        self.iam_user_alice = IamUser(arn=f"arn:aws:iam::{aws_account_id}:user/alice")
        self.iam_group_admin = IamGroup(arn=f"arn:aws:iam::{aws_account_id}:group/Admin")

        self.principal_list: List[Iam] = [
            self.iam_role_ec2_web_app,
            self.iam_service_role_ecs,
            self.iam_user_alice,
            self.iam_group_admin,
        ]

        # --- Resource
        self.db_amz = Database(account_id="111122223333", region="us-east-1", name="amz")
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

        self.tag_admin_y = LfTag(key="admin", value="y")
        self.tag_admin_n = LfTag(key="admin", value="n")
        self.tag_regular_y = LfTag(key="regular", value="y")
        self.tag_regular_n = LfTag(key="regular", value="n")
        self.tag_limited_y = LfTag(key="limited", value="y")
        self.tag_limited_n = LfTag(key="limited", value="n")

        self.tag_list: List[LfTag] = [
            self.tag_admin_y,
            self.tag_admin_n,
            self.tag_regular_y,
            self.tag_regular_n,
            self.tag_limited_y,
            self.tag_limited_n,
        ]
        self.resource_list: List[Resource] = self.db_list + self.tb_list + self.col_list + self.tag_list

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
