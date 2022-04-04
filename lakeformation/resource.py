# -*- coding: utf-8 -*-

"""
Ref:

- List database: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_databases
- Get database: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_database
- List table: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_tables
- Get table: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue.html#Glue.Client.get_table
"""

from typing import (
    List, Tuple, Set, Dict, Iterable, Sequence, Mapping,
    Union, Any, Optional, Type, TYPE_CHECKING
)
from box import Box

from .abstract import HashableAbc, RenderableAbc, SerializableAbc
from .validator import validate_attr_type
from .utils import to_var_name
from .constant import DELIMITER

if TYPE_CHECKING:  # pragma: no cover
    from .pb.playbook import Playbook
    from .pb.asso import DataLakePermission


class Resource(HashableAbc, RenderableAbc, SerializableAbc):
    res_type: str = None  # Resource Type identifier

    @classmethod
    def deserialize(cls, data: dict) -> Union[
        'Database', 'Table', 'Column', 'LfTag'
    ]:
        return _resource_type_mapper[data["res_type"]].deserialize(data)

    @property
    def get_add_remove_lf_tags_arg_name(self) -> str:
        """
        Argument name for AWS Boto3 lakeformation client:

        - add_lf_tags_to_resource
        - remove_lf_tags_from_resource
        - get_resource_lf_tags
        """
        raise NotImplementedError

    @property
    def get_add_remove_lf_tags_arg_value(self) -> dict:
        """
        Argument value for AWS Boto3 lakeformation client:

        - add_lf_tags_to_resource
        - remove_lf_tags_from_resource
        - get_resource_lf_tags
        """
        raise NotImplementedError

    @property
    def get_batch_grant_permission_arg_name(self) -> str:
        raise NotImplementedError

    def get_batch_grant_permission_arg_value(
        self,
        dl_permission: 'DataLakePermission',
    ) -> dict:
        raise NotImplementedError


class NonLfTagResource(Resource):
    pass


class Database(NonLfTagResource):
    res_type: str = "Database"

    def __init__(
        self,
        account_id: str,
        region: str,
        name: str,
    ):
        self.account_id = account_id
        self.region = region
        self.name = name
        self.validate()

        self.t: Dict[str, Table] = Box()

    def validate(self):
        validate_attr_type(self, "account_id", self.account_id, str)
        validate_attr_type(self, "region", self.region, str)
        validate_attr_type(self, "name", self.name, str)

    @property
    def attr_name(self) -> str:
        return to_var_name(f"{self.account_id}_{self.region}_{self.name}")

    @property
    def var_name(self) -> str:
        return f"db_{self.attr_name}"

    def __repr__(self):
        return f"{self.__class__.__name__}(account_id={self.account_id!r}, region={self.region!r}, name={self.name!r})"

    @property
    def id(self) -> str:
        return self.var_name

    def serialize(self) -> dict:
        return dict(
            res_type=self.res_type,
            account_id=self.account_id,
            region=self.region,
            name=self.name,
        )

    @classmethod
    def deserialize(cls, data: dict) -> 'Database':
        return cls(
            account_id=data["account_id"],
            region=data["region"],
            name=data["name"],
        )

    @property
    def get_add_remove_lf_tags_arg_name(self) -> str:
        return "Database"

    @property
    def get_add_remove_lf_tags_arg_value(self) -> dict:
        return dict(
            CatalogId=self.account_id,
            Name=self.name,
        )


class Table(NonLfTagResource):
    res_type: str = "Table"

    def __init__(
        self,
        name: str,
        database: Database,
    ):
        self.name = name
        self.database = database
        self.validate()

        self.c: Dict[str, Column] = Box()

    def validate(self):
        validate_attr_type(self, "name", self.name, str)
        validate_attr_type(self, "database", self.database, Database)

    @property
    def attr_name(self) -> str:
        return to_var_name(self.name)

    @property
    def var_name(self) -> str:
        return f"tb_{self.database.attr_name}_{self.attr_name}"

    def __repr__(self):
        return f"Table(database={self.database!r}, name={self.name!r})"

    @property
    def id(self) -> str:
        return self.var_name

    def serialize(self) -> dict:
        return dict(
            res_type=self.res_type,
            name=self.name,
            database=self.database.serialize(),
        )

    @classmethod
    def deserialize(cls, data: dict) -> 'Table':
        return cls(
            name=data["name"],
            database=Database.deserialize(data["database"]),
        )

    @property
    def get_add_remove_lf_tags_arg_name(self) -> str:
        return "Table"

    @property
    def get_add_remove_lf_tags_arg_value(self) -> dict:
        return dict(
            CatalogId=self.database.account_id,
            DatabaseName=self.database.name,
            Name=self.name,
        )


class Column(NonLfTagResource):
    res_type: str = "Column"

    def __init__(
        self,
        name: str,
        table: Table,
    ):
        self.name = name
        self.table = table
        self.validate()

    def validate(self):
        validate_attr_type(self, "name", self.name, str)
        validate_attr_type(self, "table", self.table, Table)

    @property
    def attr_name(self) -> str:
        return to_var_name(self.name)

    @property
    def var_name(self) -> str:
        return f"col_{self.table.database.attr_name}_{self.table.attr_name}_{self.attr_name}"

    def __repr__(self):
        return f'Column(table={self.table!r}, name={self.name!r})'

    @property
    def id(self) -> str:
        return self.var_name

    def serialize(self) -> dict:
        return dict(
            res_type=self.res_type,
            name=self.name,
            table=self.table.serialize(),
        )

    @classmethod
    def deserialize(cls, data: dict) -> 'Column':
        return cls(
            name=data["name"],
            table=Table.deserialize(data["table"]),
        )

    @property
    def get_add_remove_lf_tags_arg_name(self) -> str:
        return "TableWithColumns"

    @property
    def get_add_remove_lf_tags_arg_value(self) -> dict:
        return dict(
            CatalogId=self.table.database.account_id,
            DatabaseName=self.table.database.name,
            Name=self.table.name,
            ColumnNames=[self.name, ]
        )


class LfTag(Resource):
    res_type: str = "LfTag"

    def __init__(
        self,
        key: str,
        value: str,
        pb: 'Playbook' = None,
    ):
        self.key = key
        self.value = value
        self.validate()

        if pb is not None: # pragma: no cover
            pb.add_tag(self)
        self.pb = pb

    def validate(self):
        validate_attr_type(self, "key", self.key, str)
        validate_attr_type(self, "value", self.value, str)

    @property
    def id(self):
        return f"tag_{self.key}_{self.value}"

    @property
    def var_name(self):
        return f"lf_tag_{self.key.lower()}_{self.value.lower()}"

    def __repr__(self):
        return f"{self.__class__.__name__}(key={self.key!r}, value={self.value!r})"

    def serialize(self) -> dict:
        return dict(
            res_type=self.res_type,
            key=self.key,
            value=self.value,
        )

    @classmethod
    def deserialize(cls, data: dict) -> 'LfTag':
        return cls(key=data["key"], value=data["value"])

    @property
    def get_batch_grant_permission_arg_name(self) -> str:
        return "LFTagPolicy"

    def get_batch_grant_permission_arg_value(
        self,
        dl_permission: 'DataLakePermission',
    ) -> dict:
        return dict(
            CatalogId=self.pb.account_id,
            ResourceType=dl_permission.permission.resource_type,
            Expression=[
                dict(
                    TagKey=self.key,
                    TagValues=[self.value, ],
                ),
            ]
        )


_resource_type_mapper: Dict[str, Type['Resource']] = {
    "Database": Database,
    "Table": Table,
    "Column": Column,
    "LfTag": LfTag,
}
