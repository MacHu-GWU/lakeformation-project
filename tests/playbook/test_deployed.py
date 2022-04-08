# -*- coding: utf-8 -*-

import boto3
import pytest
from lakeformation.tests import AWS
from lakeformation.pb.deployed import (
    list_all_iam_role,
    list_all_iam_user,
    list_all_iam_group,
    list_all_db_tb_col,
    list_all_datalake_location,
)

aws = AWS()


def setup_module(model):
    aws.create_all()


def teardown_module(model):
    aws.delete_all()


def test():
    pass


def test_list_all_iam_role():
    arn_list = [role.arn for role in list_all_iam_role(aws.iam_client)]
    assert aws.iam_role.arn in arn_list


def test_list_all_iam_user():
    arn_list = [user.arn for user in list_all_iam_user(aws.iam_client)]
    assert aws.iam_user.arn in arn_list


def test_list_all_iam_group():
    arn_list = [group.arn for group in list_all_iam_group(aws.iam_client)]
    assert aws.iam_group.arn in arn_list


def test_list_all_db_tb_col():
    res_id_list = [
        res.id
        for res in list_all_db_tb_col(
            aws.glue_client,
            aws_account_id=aws.aws_account_id,
            aws_region=aws.aws_region,
        )
    ]
    assert aws.db.id in res_id_list
    assert aws.tb.id in res_id_list


def test_list_all_datalake_location():
    dl_loc_list = [
        dl_loc.id
        for dl_loc in list_all_datalake_location(
            aws.lf_client,
            aws_account_id=aws.aws_account_id,
        )
    ]
    assert aws.dl_loc.id in dl_loc_list


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
