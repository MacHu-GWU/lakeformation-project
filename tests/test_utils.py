# -*- coding: utf-8 -*-

import pytest
from datetime import timezone
from lakeformation.utils import (
    to_var_name,
    get_local_and_utc_now,
    get_diff_and_inter,
    grouper_list
)


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


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
