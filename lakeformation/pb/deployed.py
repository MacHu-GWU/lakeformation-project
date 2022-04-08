# -*- coding: utf-8 -*-

import boto3
from typing import List, Union

from .asso import LfTagAttachment, DataLakePermission
from ..boto_utils import list_recursively
from ..principal import (
    Principal, IamRole, IamUser, IamGroup, ExternalAccount
)
from ..resource import (
    Resource, Database, Table, Column,
    DataLakeLocation, DataCellsFilter, LfTag,
)


def list_all_iam_role(iam_client) -> List[IamRole]:
    iam_role_list = list()
    for role_dct in list_recursively(
        method=iam_client.list_roles,
        default_kwargs=dict(
            MaxItems=1000,
        ),
        next_token_arg_name="Marker",
        next_token_value_field="Marker",
        collection_value_field="Roles"
    ):
        role = IamRole(arn=role_dct["Arn"])
        iam_role_list.append(role)
    return iam_role_list


def list_all_iam_user(iam_client) -> List[IamUser]:
    iam_user_list = list()
    for user_dct in list_recursively(
        method=iam_client.list_users,
        default_kwargs=dict(
            MaxItems=1000,
        ),
        next_token_arg_name="Marker",
        next_token_value_field="Marker",
        collection_value_field="Users"
    ):
        user = IamUser(arn=user_dct["Arn"])
        iam_user_list.append(user)
    return iam_user_list


def list_all_iam_group(iam_client) -> List[IamGroup]:
    iam_group_list = list()
    for group_dct in list_recursively(
        method=iam_client.list_groups,
        default_kwargs=dict(
            MaxItems=1000,
        ),
        next_token_arg_name="Marker",
        next_token_value_field="Marker",
        collection_value_field="Groups",
    ):
        group = IamGroup(arn=group_dct["Arn"])
        iam_group_list.append(group)
    return iam_group_list


# def list_all_datalake_permission(lf_client) -> List[DataLakePermission]:
#     for db_dct in list_permissions(
#         method=glue_client.get_databases,
#         default_kwargs=dict(
#             CatalogId=aws_account_id,
#             MaxResults=1000,
#             ResourceShareType="ALL",
#         ),
#         next_token_arg_name="NextToken",
#         next_token_value_field="NextToken",
#         collection_value_field="DatabaseList"
#     ):


def list_all_db_tb_col(
    glue_client,
    aws_account_id: str,
    aws_region: str,
) -> List[Union[Database, Table, Column]]:
    res_list = list()

    for db_dct in list_recursively(
        method=glue_client.get_databases,
        default_kwargs=dict(
            CatalogId=aws_account_id,
            MaxResults=1000,
            ResourceShareType="ALL",
        ),
        next_token_arg_name="NextToken",
        next_token_value_field="NextToken",
        collection_value_field="DatabaseList"
    ):
        db = Database(
            catalog_id=db_dct["CatalogId"],
            region=aws_region,
            name=db_dct["Name"],
        )
        res_list.append(db)
        for tb_dct in list_recursively(
            method=glue_client.get_tables,
            default_kwargs=dict(
                CatalogId=db.catalog_id,
                DatabaseName=db.name,
                MaxResults=1000,
            ),
            next_token_arg_name="NextToken",
            next_token_value_field="NextToken",
            collection_value_field="TableList"
        ):
            tb = Table(
                name=tb_dct["Name"],
                database=db,
            )
            res_list.append(tb)

            for col_dct in tb_dct.get("StorageDescriptor", dict()).get("Columns", []):
                column = Column(name=col_dct["Name"], table=tb)
                res_list.append(column)

    return res_list


def list_all_datalake_location(
    lf_client,
    aws_account_id: str,
) -> List[DataLakeLocation]:
    dl_loc_list = list()
    for dl_loc_dct in list_recursively(
        method=lf_client.list_resources,
        default_kwargs=dict(
            MaxResults=1000,
        ),
        next_token_arg_name="NextToken",
        next_token_value_field="NextToken",
        collection_value_field="ResourceInfoList"
    ):
        role_arn = dl_loc_dct["RoleArn"]
        if role_arn.endswith("AWSServiceRoleForLakeFormationDataAccess"):
            role_arn = None
        dl_loc = DataLakeLocation(
            catalog_id=aws_account_id,
            resource_arn=dl_loc_dct["ResourceArn"],
            role_arn=role_arn,
        )
        dl_loc_list.append(dl_loc)
    return dl_loc_list

    # for lf_dct in list_recursively(
    #     method=lf_client.list_lf_tags,
    #     default_kwargs=dict(
    #         CatalogId=aws_account_id,
    #         ResourceShareType="ALL",
    #         MaxResults=1000,
    #     ),
    #     next_token_arg_name="NextToken",
    #     next_token_value_field="NextToken",
    #     collection_value_field="LFTags"
    # ):
    #     for value in lf_dct.get("TagValues", list()):
    #         tag = LfTag(
    #             catalog_id=aws_account_id,
    #             key=lf_dct["TagKey"],
    #             value=value,
    #         )
    #         res_list.append(tag)

    return res_list


def list_all_principal(iam_client) -> List[Principal]:
    principal_list = list()

    iam_role_list = list_all_iam_role(iam_client)
    iam_user_list = list_all_iam_user(iam_client)
    iam_group_list = list_all_iam_group(iam_client)

    principal_list.extend(iam_role_list)
    principal_list.extend(iam_user_list)
    principal_list.extend(iam_group_list)

    return principal_list
