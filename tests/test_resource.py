# -*- coding: utf-8 -*-

import pytest
from lakeformation.resource import (
    Resource, Database, Table, Column, LfTag
)
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


def test_render():
    assert obj.db_amz.var_name == "db_111122223333_us_east_1_amz"
    assert obj.tb_amz_user.var_name == "tb_111122223333_us_east_1_amz_user"
    assert obj.col_amz_user_id.var_name == "col_111122223333_us_east_1_amz_user_id"

    assert repr(obj.db_amz) == "Database(account_id='111122223333', region='us-east-1', name='amz')"
    assert repr(
        obj.tb_amz_user) == "Table(database=Database(account_id='111122223333', region='us-east-1', name='amz'), name='user')"
    assert repr(
        obj.col_amz_user_id) == "Column(table=Table(database=Database(account_id='111122223333', region='us-east-1', name='amz'), name='user'), name='id')"


def test_seder():
    assert Database.deserialize(obj.db_amz.serialize()) == obj.db_amz
    assert Table.deserialize(obj.tb_amz_user.serialize()) == obj.tb_amz_user
    assert Column.deserialize(obj.col_amz_user_id.serialize()) == obj.col_amz_user_id

    for r in obj.resource_list:
        assert Resource.deserialize(r.serialize()) == r


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
