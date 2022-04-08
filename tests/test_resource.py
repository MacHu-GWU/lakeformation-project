# -*- coding: utf-8 -*-

import pytest
from lakeformation.resource import (
    Resource, Database, Table, Column, DataLakeLocation, DataCellsFilter, LfTag
)
from lakeformation.permission import PermissionEnum
from lakeformation.pb.playbook import Playbook
from lakeformation.pb.asso import DataLakePermission
from lakeformation.tests import Objects

obj = Objects()


def test_hash():
    _ = set(obj.resource_list)

    obj1 = Objects()
    obj2 = Objects()

    for r1, r2 in zip(obj1.resource_list, obj2.resource_list):
        assert r1 == r2
        assert r1.id == r2.id
        assert hash(r1) == hash(r2)

    assert obj1.db_amz != obj1.tb_amz_user


def test_property():
    assert obj.db_amz.catalog_id == obj.tb_amz_user.catalog_id
    assert obj.db_amz.catalog_id == obj.col_amz_user_id.catalog_id
    assert obj.db_amz.catalog_id == obj.col_amz_user_password.catalog_id


def test_render():
    assert obj.db_amz.var_name == "db_111122223333_us_east_1_amz"
    assert obj.tb_amz_user.var_name == "tb_111122223333_us_east_1_amz_user"
    assert obj.col_amz_user_id.var_name == "col_111122223333_us_east_1_amz_user_id"

    assert repr(obj.db_amz) == "Database(catalog_id='111122223333', region='us-east-1', name='amz')"
    assert repr(
        obj.tb_amz_user) == "Table(database=Database(catalog_id='111122223333', region='us-east-1', name='amz'), name='user')"
    assert repr(
        obj.col_amz_user_id) == "Column(table=Table(database=Database(catalog_id='111122223333', region='us-east-1', name='amz'), name='user'), name='id')"


def test_seder():
    assert Database.deserialize(obj.db_amz.serialize()) == obj.db_amz
    assert Table.deserialize(obj.tb_amz_user.serialize()) == obj.tb_amz_user
    assert Column.deserialize(obj.col_amz_user_id.serialize()) == obj.col_amz_user_id

    for r in obj.resource_list:
        assert Resource.deserialize(r.serialize()) == r


class TestResource:
    def test_get_add_remove_lf_tags_arg(self):
        """
        Verify those methods are implemented
        """
        _ = obj.db_amz.get_add_remove_lf_tags_arg_name
        _ = obj.db_amz.get_add_remove_lf_tags_arg_value
        _ = obj.tb_amz_user.get_add_remove_lf_tags_arg_name
        _ = obj.tb_amz_user.get_add_remove_lf_tags_arg_value
        _ = obj.col_amz_user_id.get_add_remove_lf_tags_arg_name
        _ = obj.col_amz_user_id.get_add_remove_lf_tags_arg_value

    def test_batch_grant_remove_permission_arg(self):
        _ = obj.db_amz.batch_grant_remove_permission_arg_name
        _ = obj.db_amz.batch_grant_remove_permission_arg_value()
        _ = obj.tb_amz_user.batch_grant_remove_permission_arg_name
        _ = obj.tb_amz_user.batch_grant_remove_permission_arg_value()
        _ = obj.col_amz_user_id.batch_grant_remove_permission_arg_name
        _ = obj.col_amz_user_id.batch_grant_remove_permission_arg_value()

        _ = obj.tag_admin_y.batch_grant_remove_permission_arg_name
        _ = obj.tag_admin_y.batch_grant_remove_permission_arg_value(obj.dl_permission_iam_user_alice_tag_admin_y)
        _ = obj.dl_loc.batch_grant_remove_permission_arg_name
        _ = obj.dl_loc.batch_grant_remove_permission_arg_value()
        _ = obj.data_filter.batch_grant_remove_permission_arg_name
        _ = obj.data_filter.batch_grant_remove_permission_arg_value()


class TestDataLakeLocation:
    def test_init(self):
        _ = DataLakeLocation(
            catalog_id=obj.aws_account_id,
            resource_arn=obj.dl_loc.resource_arn,
        )
        _ = DataLakeLocation(
            catalog_id=obj.aws_account_id,
            resource_arn=obj.dl_loc.resource_arn,
            role_arn=obj.iam_role_ec2_web_app.arn,
        )


class TestDataCellFilter:
    def test_init(self):
        _ = DataCellsFilter(
            filter_name="", catalog_id="", database_name="", table_name="",
            column_level_access=DataCellsFilter.ColumnLevelAccessEnum.all,
            row_filter_expression="has_pii = false",
        )
        _ = DataCellsFilter(
            filter_name="", catalog_id="", database_name="", table_name="",
            column_level_access=DataCellsFilter.ColumnLevelAccessEnum.include,
            include_columns=["a"],
        )
        _ = DataCellsFilter(
            filter_name="", catalog_id="", database_name="", table_name="",
            column_level_access=DataCellsFilter.ColumnLevelAccessEnum.exclude,
            exclude_columns=["a"],
        )

        with pytest.raises(ValueError):
            _ = DataCellsFilter(
                filter_name="", catalog_id="", database_name="", table_name="",
                column_level_access=DataCellsFilter.ColumnLevelAccessEnum.all,
                include_columns=["a", ],
                row_filter_expression="has_pii = false",
            )
        with pytest.raises(ValueError):
            _ = DataCellsFilter(
                filter_name="", catalog_id="", database_name="", table_name="",
                column_level_access=DataCellsFilter.ColumnLevelAccessEnum.all,
                exclude_columns=["a", ],
                row_filter_expression="has_pii = false",
            )

        with pytest.raises(ValueError):
            _ = DataCellsFilter(
                filter_name="", catalog_id="", database_name="", table_name="",
                column_level_access=DataCellsFilter.ColumnLevelAccessEnum.include,
                include_columns=None,
                row_filter_expression="has_pii = false",
            )
        with pytest.raises(ValueError):
            _ = DataCellsFilter(
                filter_name="", catalog_id="", database_name="", table_name="",
                column_level_access=DataCellsFilter.ColumnLevelAccessEnum.include,
                exclude_columns=["a", ],
                row_filter_expression="has_pii = false",
            )

        with pytest.raises(ValueError):
            _ = DataCellsFilter(
                filter_name="", catalog_id="", database_name="", table_name="",
                column_level_access=DataCellsFilter.ColumnLevelAccessEnum.exclude,
                exclude_columns=None,
                row_filter_expression="has_pii = false",
            )
        with pytest.raises(ValueError):
            _ = DataCellsFilter(
                filter_name="", catalog_id="", database_name="", table_name="",
                column_level_access=DataCellsFilter.ColumnLevelAccessEnum.exclude,
                include_columns=["a", ],
                row_filter_expression="has_pii = false",
            )

        with pytest.raises(ValueError):
            _ = DataCellsFilter(
                filter_name="", catalog_id="", database_name="", table_name="",
                column_level_access="invalid",
            )


class TestLfTag:
    def test_hash(self):
        obj1 = Objects()
        obj2 = Objects()
        _ = set(obj.tag_list)

        for tag1, tag2 in zip(obj1.tag_list, obj2.tag_list):
            assert tag1 == tag2
            assert tag1.id == tag2.id
            assert hash(tag1) == hash(tag2)

        assert obj1.tag_admin_y != obj1.tag_admin_n

    def test_serde(self):
        for tag in obj.tag_list:
            assert LfTag.deserialize(tag.serialize()) == tag


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
