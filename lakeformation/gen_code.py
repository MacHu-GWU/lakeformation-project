# -*- coding: utf-8 -*-

from pathlib import Path
from typing import List

from jinja2 import Template

from .resource import Resource, Database, Table, Column
from .principal import Principal, IamRole, IamUser, IamGroup

dir_here = Path(__file__).absolute().parent
tpl_resource = Path(dir_here, "tpl", "resource.tpl")
tpl_principal = Path(dir_here, "tpl", "principal.tpl")


def gen_resource(boto_ses, workspace_dir: str):
    sts_client = boto_ses.client("sts")
    glue_client = boto_ses.client("glue")

    account_id = sts_client.get_caller_identity()["Account"]
    region_name = boto_ses.region_name

    database_list: List[Database] = list()
    db_response = glue_client.get_databases(
        CatalogId=account_id,
        MaxResults=1000,
    )
    for db_dct in db_response.get("DatabaseList", []):
        database = Database(
            account_id=account_id,
            region=region_name,
            name=db_dct["Name"],
        )

        tb_response = glue_client.get_tables(
            CatalogId=account_id,
            DatabaseName=db_dct["Name"],
            MaxResults=1000,
        )

        for tb_dct in tb_response.get("TableList", []):
            table = Table(
                name=tb_dct["Name"],
                database=database,
            )

            for col_dct in tb_dct["StorageDescriptor"].get("Columns", []):
                column = Column(name=col_dct["Name"], table=table)
                table.c[column.name] = column

            database.t[table.name] = table

        database_list.append(database)

    tpl = Template(source=tpl_resource.read_text(encoding="utf-8"))
    content = tpl.render(database_list=database_list)

    filename = f"resource_{account_id}_{region_name.replace('-', '_')}.py"
    output_path = Path(workspace_dir, filename)
    output_path.write_text(content, encoding="utf-8")


def gen_principal(boto_ses, workspace_dir: str):
    sts_client = boto_ses.client("sts")
    iam_client = boto_ses.client("iam")

    account_id = sts_client.get_caller_identity()["Account"]

    iam_user_list: List[IamUser] = list()
    iam_group_list: List[IamGroup] = list()
    iam_role_list: List[IamRole] = list()

    list_users_response = iam_client.list_users(
        MaxItems=1000,
    )
    for user_dct in list_users_response.get("Users", []):
        iam_user = IamUser(arn=user_dct["Arn"])
        iam_user_list.append(iam_user)

    list_groups_response = iam_client.list_groups(
        MaxItems=1000,
    )
    for group_dct in list_groups_response.get("Groups", []):
        iam_group = IamGroup(arn=group_dct["Arn"])
        iam_group_list.append(iam_group)

    list_roles_response = iam_client.list_roles(
        MaxItems=1000,
    )
    for role_dct in list_roles_response.get("Roles", []):
        iam_role = IamRole(arn=role_dct["Arn"])
        iam_role_list.append(iam_role)

    tpl = Template(source=tpl_principal.read_text(encoding="utf-8"))
    content = tpl.render(
        iam_user_list=iam_user_list,
        iam_group_list=iam_group_list,
        iam_role_list=iam_role_list,
    )

    filename = f"principal_{account_id}.py"
    output_path = Path(workspace_dir, filename)
    output_path.write_text(content, encoding="utf-8")
