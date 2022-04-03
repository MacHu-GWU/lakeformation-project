# -*- coding: utf-8 -*-

import pytest
from lakeformation.principal import (
    validate_iam_arn, Iam, IamRole, IamUser, IamGroup,
)
from lakeformation.tests import Objects

obj = Objects()


def test_validate_iam_arn():
    for principal in obj.principal_list:
        validate_iam_arn(principal.arn)

    bad_arn_list = [
        "arn:aws:s3:::my-bucket"
        "arn:aws:s3::aaaabbbbcccc"
        "arn:aws:s3::111122223333:persona/admin"
    ]
    for arn in bad_arn_list:
        with pytest.raises(ValueError):
            validate_iam_arn(arn)


def test_hash():
    obj1 = Objects()
    obj2 = Objects()
    _ = set(obj.principal_list)

    for p1, p2 in zip(obj1.principal_list, obj2.principal_list):
        assert p1 == p2
        assert p1.id == p2.id
        assert hash(p1) == hash(p2)

    assert obj1.iam_role_ec2_web_app != obj1.iam_user_alice


def test_render():
    assert obj.iam_role_ec2_web_app.var_name == "role_ec2_web_app"
    assert obj.iam_service_role_ecs.var_name == "role_aws_service_role__ecs_amazonaws_com__AWSServiceRoleForECS"
    assert obj.iam_user_alice.var_name == "user_alice"
    assert obj.iam_group_admin.var_name == "group_Admin"

    assert repr(obj.iam_role_ec2_web_app) == f"IamRole(arn='{obj.iam_role_ec2_web_app.arn}')"
    assert repr(obj.iam_service_role_ecs) == f"IamRole(arn='{obj.iam_service_role_ecs.arn}')"
    assert repr(obj.iam_user_alice) == f"IamUser(arn='{obj.iam_user_alice.arn}')"
    assert repr(obj.iam_group_admin) == f"IamGroup(arn='{obj.iam_group_admin.arn}')"


def test_seder():
    assert IamRole.deserialize(obj.iam_role_ec2_web_app.serialize()) == obj.iam_role_ec2_web_app
    assert IamRole.deserialize(obj.iam_service_role_ecs.serialize()) == obj.iam_service_role_ecs
    assert IamUser.deserialize(obj.iam_user_alice.serialize()) == obj.iam_user_alice
    assert IamGroup.deserialize(obj.iam_group_admin.serialize()) == obj.iam_group_admin

    for p in obj.principal_list:
        assert Iam.deserialize(p.serialize()) == p


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
