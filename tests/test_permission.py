# -*- coding: utf-8 -*-

import pytest
from lakeformation.permission import Permission, PermissionEnum


class TestPermission:
    def test_validate(self):
        PermissionEnum._validate()

    def test_seder(self):
        assert PermissionEnum.Select.value.serialize() == {
            "identifier": "Select",
            "resource_type": "TABLE",
            "permission": "SELECT",
            "grantable": False,
        }
        assert Permission.deserialize(
            PermissionEnum.Select.value.serialize()
        ).serialize() == PermissionEnum.Select.value.serialize()


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
