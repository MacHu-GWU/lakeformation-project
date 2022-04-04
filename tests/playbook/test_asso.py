# -*- coding: utf-8 -*-

import pytest
from lakeformation.exc import ValidationError
from lakeformation.permission import PermissionEnum
from lakeformation.pb.asso import DataLakePermission, LfTagAttachment
from lakeformation.tests import Objects

obj = Objects()


class TestDataLakePermission:
    def test_validate(self):
        _ = DataLakePermission(obj.iam_role_ec2_web_app, obj.tag_admin_y, PermissionEnum.SuperDatabase.value)

        with pytest.raises(ValidationError):
            DataLakePermission(obj.iam_role_ec2_web_app, obj.tag_admin_y, None)

        with pytest.raises(ValidationError):
            DataLakePermission(obj.iam_role_ec2_web_app, None, None)

        with pytest.raises(ValidationError):
            DataLakePermission(None, None, None)

    def test_hash(self):
        obj1 = Objects()
        obj2 = Objects()
        assert obj1.dl_permission_iam_user_alice_tag_admin_y == obj2.dl_permission_iam_user_alice_tag_admin_y
        assert obj1.dl_permission_iam_user_alice_tag_admin_y.id == obj2.dl_permission_iam_user_alice_tag_admin_y.id
        assert hash(obj1.dl_permission_iam_user_alice_tag_admin_y) == hash(
            obj2.dl_permission_iam_user_alice_tag_admin_y)


class TestLfTagAttachment:
    def test_validate(self):
        _ = LfTagAttachment(obj.db_amz, obj.tag_admin_y)

        with pytest.raises(ValidationError):
            LfTagAttachment(obj.db_amz, obj.db_amz)

        with pytest.raises(ValidationError):
            LfTagAttachment(obj.tag_admin_y, obj.tag_admin_y)

        with pytest.raises(ValidationError):
            LfTagAttachment(obj.tag_admin_y, obj.db_amz)

    def test_hash(self):
        obj1 = Objects()
        obj2 = Objects()
        assert obj1.attachment_db_amz_tag_admin_y == obj2.attachment_db_amz_tag_admin_y
        assert obj1.attachment_db_amz_tag_admin_y.id == obj2.attachment_db_amz_tag_admin_y.id
        assert hash(obj1.attachment_db_amz_tag_admin_y) == hash(obj2.attachment_db_amz_tag_admin_y)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
