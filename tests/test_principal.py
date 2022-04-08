# -*- coding: utf-8 -*-

import pytest
from lakeformation.principal import (
    Principal,
    IamRole, IamUser, IamGroup,
    ExternalAccount,
)
from lakeformation.tests import Objects

obj = Objects()


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
    assert obj.acc1.var_name == "acc_111111111111"
    assert obj.acc2.var_name == "acc_222222222222"

    assert repr(obj.iam_role_ec2_web_app) == f"IamRole(arn='{obj.iam_role_ec2_web_app.arn}')"
    assert repr(obj.iam_service_role_ecs) == f"IamRole(arn='{obj.iam_service_role_ecs.arn}')"
    assert repr(obj.iam_user_alice) == f"IamUser(arn='{obj.iam_user_alice.arn}')"
    assert repr(obj.iam_group_admin) == f"IamGroup(arn='{obj.iam_group_admin.arn}')"
    assert repr(obj.acc1) == f"ExternalAccount(account_id='{obj.acc1.account_id}')"
    assert repr(obj.acc2) == f"ExternalAccount(account_id='{obj.acc2.account_id}')"


def test_seder():
    assert IamRole.deserialize(obj.iam_role_ec2_web_app.serialize()) == obj.iam_role_ec2_web_app
    assert IamRole.deserialize(obj.iam_service_role_ecs.serialize()) == obj.iam_service_role_ecs
    assert IamUser.deserialize(obj.iam_user_alice.serialize()) == obj.iam_user_alice
    assert IamGroup.deserialize(obj.iam_group_admin.serialize()) == obj.iam_group_admin
    assert ExternalAccount.deserialize(obj.acc1.serialize()) == obj.acc1
    assert ExternalAccount.deserialize(obj.acc2.serialize()) == obj.acc2

    for p in obj.principal_list:
        assert Principal.deserialize(p.serialize()) == p


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
