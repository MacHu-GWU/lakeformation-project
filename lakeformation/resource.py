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

from .abstract import HashableAbc, RenderableAbc, SerializableAbc, PlaybookManaged
from .validator import validate_attr_type
from .utils import to_var_name, validate_account_id, validate_iam_arn
from .constant import DELIMITER

if TYPE_CHECKING:  # pragma: no cover
    from .pb.playbook import Playbook
    from .pb.asso import DataLakePermission


class Resource(HashableAbc, RenderableAbc, SerializableAbc, PlaybookManaged):
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
    def batch_grant_remove_permission_arg_name(self) -> str:
        raise NotImplementedError

    def batch_grant_remove_permission_arg_value(
        self,
        dl_permission: 'DataLakePermission',
    ) -> dict:
        raise NotImplementedError


class NonLfTagResource(Resource):
    pass


class Database(NonLfTagResource):
    object_type: str = "Database"

    def __init__(
        self,
        catalog_id: str,
        region: str,
        name: str,
        _playbook_id: Optional[str] = None,
    ):
        self.catalog_id = catalog_id
        self.region = region
        self.name = name
        self._playbook_id = _playbook_id
        self.validate()

        self.t: Dict[str, Table] = Box()

    def validate(self):
        validate_attr_type(self, "catalog_id", self.catalog_id, str)
        validate_attr_type(self, "region", self.region, str)
        validate_attr_type(self, "name", self.name, str)
        validate_account_id(self.catalog_id)

    @property
    def attr_name(self) -> str:
        return to_var_name(f"{self.catalog_id}_{self.region}_{self.name}")

    @property
    def var_name(self) -> str:
        return f"db_{self.attr_name}"

    def __repr__(self):
        return f"{self.__class__.__name__}(catalog_id={self.catalog_id!r}, region={self.region!r}, name={self.name!r})"

    @property
    def id(self) -> str:
        return self.var_name

    def serialize(self) -> dict:
        return dict(
            object_type=self.object_type,
            catalog_id=self.catalog_id,
            region=self.region,
            name=self.name,
            _playbook_id=self._playbook_id,
        )

    @classmethod
    def deserialize(cls, data: dict) -> 'Database':
        return cls(
            catalog_id=data["catalog_id"],
            region=data["region"],
            name=data["name"],
            _playbook_id=data["_playbook_id"],
        )

    @property
    def get_add_remove_lf_tags_arg_name(self) -> str:
        return "Database"

    @property
    def get_add_remove_lf_tags_arg_value(self) -> dict:
        return dict(
            CatalogId=self.catalog_id,
            Name=self.name,
        )

    @property
    def batch_grant_remove_permission_arg_name(self) -> str:
        return "Database"

    def batch_grant_remove_permission_arg_value(
        self,
        dl_permission: 'DataLakePermission' = None,
    ) -> dict:
        return dict(
            CatalogId=self.catalog_id,
            Name=self.name
        )


class Table(NonLfTagResource):
    object_type: str = "Table"

    def __init__(
        self,
        name: str,
        database: Database,
        _playbook_id: Optional[str] = None,
    ):
        self.name = name
        self.database = database
        self._playbook_id = _playbook_id
        self.validate()

        self.c: Dict[str, Column] = Box()

    def validate(self):
        validate_attr_type(self, "name", self.name, str)
        validate_attr_type(self, "database", self.database, Database)

    @property
    def catalog_id(self) -> str:
        return self.database.catalog_id

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
            object_type=self.object_type,
            name=self.name,
            database=self.database.serialize(),
            _playbook_id=self._playbook_id,
        )

    @classmethod
    def deserialize(cls, data: dict) -> 'Table':
        return cls(
            name=data["name"],
            database=Database.deserialize(data["database"]),
            _playbook_id=data["_playbook_id"],
        )

    @property
    def get_add_remove_lf_tags_arg_name(self) -> str:
        return "Table"

    @property
    def get_add_remove_lf_tags_arg_value(self) -> dict:
        return dict(
            CatalogId=self.database.catalog_id,
            DatabaseName=self.database.name,
            Name=self.name,
        )

    @property
    def batch_grant_remove_permission_arg_name(self) -> str:
        return "Table"

    def batch_grant_remove_permission_arg_value(
        self,
        dl_permission: 'DataLakePermission' = None,
    ) -> dict:
        return dict(
            CatalogId=self.catalog_id,
            DatabaseName=self.database.name,
            Name=self.name,
        )


class Column(NonLfTagResource):
    object_type: str = "Column"

    def __init__(
        self,
        name: str,
        table: Table,
        _playbook_id: Optional[str] = None,
    ):
        self.name = name
        self.table = table
        self._playbook_id = _playbook_id
        self.validate()

    def validate(self):
        validate_attr_type(self, "name", self.name, str)
        validate_attr_type(self, "table", self.table, Table)

    @property
    def catalog_id(self) -> str:
        return self.table.catalog_id

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
            object_type=self.object_type,
            name=self.name,
            table=self.table.serialize(),
            _playbook_id=self._playbook_id,
        )

    @classmethod
    def deserialize(cls, data: dict) -> 'Column':
        return cls(
            name=data["name"],
            table=Table.deserialize(data["table"]),
            _playbook_id=data["_playbook_id"],
        )

    @property
    def get_add_remove_lf_tags_arg_name(self) -> str:
        return "TableWithColumns"

    @property
    def get_add_remove_lf_tags_arg_value(self) -> dict:
        return dict(
            CatalogId=self.table.database.catalog_id,
            DatabaseName=self.table.database.name,
            Name=self.table.name,
            ColumnNames=[self.name, ]
        )

    @property
    def batch_grant_remove_permission_arg_name(self) -> str:
        return "TableWithColumns"

    def batch_grant_remove_permission_arg_value(
        self,
        dl_permission: 'DataLakePermission' = None,
    ) -> dict:
        return dict(
            CatalogId=self.catalog_id,
            DatabaseName=self.table.database.name,
            Name=self.table.name,
            ColumnNames=[self.name, ]
        )


class DataLakeLocation(NonLfTagResource):
    """

    """
    object_type: str = "DataLakeLocation"

    def __init__(
        self,
        catalog_id: str,
        resource_arn: str,
        role_arn: str = None,
        pb: 'Playbook' = None,
        _playbook_id: Optional[str] = None,
    ):
        self.catalog_id = catalog_id
        self.resource_arn = resource_arn
        self.role_arn = role_arn
        if role_arn is None:
            self.use_service_link_role = True
        else:
            self.use_service_link_role = False
        if pb is None:
            self._playbook_id = _playbook_id
        else:
            pb.add_dl_location(self)
            self._playbook_id = pb.playbook_id
        self.pb = pb
        self.validate()

    def validate(self):
        validate_attr_type(self, "catalog_id", self.catalog_id, str)
        validate_attr_type(self, "resource_arn", self.resource_arn, str)
        validate_account_id(self.catalog_id)
        if self.role_arn is not None:
            validate_iam_arn(self.role_arn)

    @property
    def attr_name(self) -> str:
        return to_var_name(f"{self.catalog_id}_{self.resource_arn}")

    @property
    def var_name(self) -> str:
        return f"dl_loc_{self.attr_name}"

    def __repr__(self):
        return f"{self.__class__.__name__}(catalog_id={self.catalog_id!r}, resource_arn={self.resource_arn!r}, role_arn={self.role_arn!r})"

    @property
    def id(self) -> str:
        return self.var_name

    def serialize(self) -> dict:
        return dict(
            object_type=self.object_type,
            catalog_id=self.catalog_id,
            resource_arn=self.resource_arn,
            role_arn=self.role_arn,
            _playbook_id=self._playbook_id,
        )

    @classmethod
    def deserialize(cls, data: dict) -> 'DataLakeLocation':
        return cls(
            catalog_id=data["catalog_id"],
            resource_arn=data["resource_arn"],
            role_arn=data["role_arn"],
            _playbook_id=data["_playbook_id"],
        )

    @property
    def batch_grant_remove_permission_arg_name(self) -> str:
        return "DataLocation"

    def batch_grant_remove_permission_arg_value(
        self,
        dl_permission: 'DataLakePermission' = None,
    ) -> dict:
        return dict(
            CatalogId=self.catalog_id,
            ResourceArn=self.resource_arn,
        )


class DataCellsFilter(NonLfTagResource):
    """

    """
    object_type: str = "DataCellsFilter"

    def __init__(
        self,
        filter_name: str,
        catalog_id: str,
        database_name: str,
        table_name: str,
        row_filter_expression: str,
        include_columns: List[str] = None,
        exclude_columns: List[str] = None,
        pb: 'Playbook' = None,
        _playbook_id: Optional[str] = None,
    ):
        self.filter_name = filter_name
        self.catalog_id = catalog_id
        self.database_name = database_name
        self.table_name = table_name
        self.row_filter_expression = row_filter_expression
        self.include_columns = include_columns
        self.exclude_columns = exclude_columns
        if pb is None:
            self._playbook_id = None
        else:
            pb.add_data_filter(self)
            self._playbook_id = pb.playbook_id
        self.pb = pb
        self.validate()

    def validate(self):
        validate_attr_type(self, "filter_name", self.filter_name, str)
        validate_attr_type(self, "catalog_id", self.catalog_id, str)
        validate_attr_type(self, "database_name", self.database_name, str)
        validate_attr_type(self, "table_name", self.table_name, str)

        if (bool(self.include_columns) + bool(self.exclude_columns)) != 1:
            raise ValueError

    @property
    def attr_name(self) -> str:
        return to_var_name(f"{self.catalog_id}_{self.filter_name}")

    @property
    def var_name(self) -> str:
        return f"filter_{self.attr_name}"

    def __repr__(self):
        return f"{self.__class__.__name__}(filter_name={self.filter_name!r}, catalog_id={self.catalog_id!r}, database_name={self.database_name!r}, table_name={self.table_name!r}, row_filter_expression={self.row_filter_expression!r}, include_columns={self.include_columns!r}, exclude_columns={self.exclude_columns!r})"

    @property
    def id(self) -> str:
        return self.var_name

    def serialize(self) -> dict:
        return dict(
            object_type=self.object_type,
            filter_name=self.filter_name,
            catalog_id=self.catalog_id,
            database_name=self.database_name,
            table_name=self.table_name,
            row_filter_expression=self.row_filter_expression,
            include_columns=self.include_columns,
            exclude_columns=self.exclude_columns,
            _playbook_id=self._playbook_id,
        )

    @classmethod
    def deserialize(cls, data: dict) -> 'DataCellsFilter':
        return cls(
            filter_name=data["filter_name"],
            catalog_id=data["catalog_id"],
            database_name=data["database_name"],
            table_name=data["table_name"],
            row_filter_expression=data["row_filter_expression"],
            include_columns=data["include_columns"],
            exclude_columns=data["exclude_columns"],
            _playbook_id=data["_playbook_id"],
        )

    @property
    def batch_grant_remove_permission_arg_name(self) -> str:
        return "DataCellsFilter"

    def batch_grant_remove_permission_arg_value(
        self,
        dl_permission: 'DataLakePermission' = None,
    ) -> dict:
        return dict(
            TableCatalogId=self.catalog_id,
            DatabaseName=self.database_name,
            TableName=self.table_name,
            Name=self.filter_name,
        )


class LfTag(Resource):
    object_type: str = "LfTag"

    def __init__(
        self,
        catalog_id: str,
        key: str,
        value: str,
        pb: 'Playbook' = None,
        _playbook_id: Optional[str] = None,
    ):
        self.catalog_id = catalog_id
        self.key = key
        self.value = value
        self.validate()

        if pb is None:
            self._playbook_id = None
        else:
            pb.add_tag(self)
            self._playbook_id = pb.playbook_id
        self.pb = pb

    def validate(self):
        validate_attr_type(self, "catalog_id", self.catalog_id, str)
        validate_attr_type(self, "key", self.key, str)
        validate_attr_type(self, "value", self.value, str)
        validate_account_id(self.catalog_id)

    @property
    def id(self):
        return f"tag_{self.key}_{self.value}"

    @property
    def var_name(self):
        return f"lf_tag_{self.key.lower()}_{self.value.lower()}"

    def __repr__(self):
        return f"{self.__class__.__name__}(catalog_id={self.catalog_id!r}, key={self.key!r}, value={self.value!r})"

    def serialize(self) -> dict:
        return dict(
            object_type=self.object_type,
            catalog_id=self.catalog_id,
            key=self.key,
            value=self.value,
            _playbook_id=self._playbook_id,
        )

    @classmethod
    def deserialize(cls, data: dict) -> 'LfTag':
        return cls(
            catalog_id=data["catalog_id"],
            key=data["key"],
            value=data["value"],
            _playbook_id=data["_playbook_id"],
        )

    @property
    def batch_grant_remove_permission_arg_name(self) -> str:
        return "LFTagPolicy"

    def batch_grant_remove_permission_arg_value(
        self,
        dl_permission: 'DataLakePermission',
    ) -> dict:
        return dict(
            CatalogId=self.catalog_id,
            ResourceType=dl_permission.permission.resource_type,
            Expression=[
                dict(
                    TagKey=self.key,
                    TagValues=[self.value, ],
                ),
            ]
        )


_resource_type_mapper = {
    Database.object_type: Database,
    Table.object_type: Table,
    Column.object_type: Column,
    DataLakeLocation.object_type: DataLakeLocation,
    DataCellsFilter.object_type: DataCellsFilter,
    LfTag.object_type: LfTag,
}


def deserialize_resource(data: dict) -> Union[
    Database,
    Table,
    Column,
    DataLakeLocation,
    DataCellsFilter,
    LfTag,
]:
    return _resource_type_mapper[data["object_type"]].deserialize(data)
