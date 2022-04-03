# -*- coding: utf-8 -*-

import pytest
from lakeformation.lf_tag import LfTag
from lakeformation.tests import Objects

obj = Objects()


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
