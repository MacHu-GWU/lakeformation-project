# -*- coding: utf-8 -*-

import pytest
from datetime import timezone
from lakeformation.utils import (
    to_var_name,
    get_local_and_utc_now,
    get_diff_and_inter,
    grouper_list,
    validate_iam_arn,
    validate_account_id,
)
from lakeformation.tests import Objects

obj = Objects()


def test_to_var_name():
    test_cases = [
        ("us-east-1", "us_east_1"),
        ("arn:aws", "arn_aws"),
        ("a/b", "a__b"),
        ("database.table", "database_dot_table"),
    ]
    for before, after in test_cases:
        assert to_var_name(before) == after


def test_get_local_and_utc_now():
    local_now, utc_now = get_local_and_utc_now()
    assert local_now == utc_now
    assert utc_now.tzinfo == timezone.utc


def test_get_diff_and_inter():
    d1 = dict(a=1, b=2)
    d2 = dict(b=2, c=3)
    s1, s2, s3 = get_diff_and_inter(d1, d2)
    assert s1 == {"a", }
    assert s2 == {"c", }
    assert s3 == {"b", }


def test_grouper_list():
    l = [1, 2, 3, 4, 5, 6, 7]
    assert list(grouper_list(l, 3)) == [[1, 2, 3], [4, 5, 6], [7, ]]


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


def test_validate_account_id():
    good_acc_id_list = [
        "000000000000",
        "111122223333",
        "444444444444",
    ]
    for acc_id in good_acc_id_list:
        validate_account_id(acc_id)

    bad_acc_id_list = [
        "1111-2222-3333"
        "11112222333"
    ]
    for acc_id in bad_acc_id_list:
        with pytest.raises(ValueError):
            validate_account_id(acc_id)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
