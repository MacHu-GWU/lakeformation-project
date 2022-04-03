# -*- coding: utf-8 -*-

from typing import (
    List, Tuple, Set, Dict, Iterable, Sequence, Mapping,
    Union, Any, Optional, Type, TYPE_CHECKING
)
from box import Box

from .abstract import HashableAbc, RenderableAbc, SerializableAbc
from .validator import validate_attr_type
from .utils import to_var_name

if TYPE_CHECKING:
    pass


class Resource(HashableAbc, RenderableAbc, SerializableAbc):
    pass


class DbTbCol(Resource):
    @classmethod
    def deserialize(cls, data: dict) -> Union['Database', 'Table', 'Column']:
        if "account_id" in data:
            return Database.deserialize(data)
        elif "database" in data:
            return Table.deserialize(data)
        elif "table" in data:
            return Column.deserialize(data)
        else:
            raise ValueError("it is not a 'Resource' deserializable dict!")

    @property
    def get_add_remove_lf_tags_arg_value(self) -> dict:
        raise NotImplementedError


class Database(Resource):
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


class Table(Resource):

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


class Column(Resource):
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
