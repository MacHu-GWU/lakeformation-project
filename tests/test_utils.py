# -*- coding: utf-8 -*-

import pytest
from lakeformation.utils import to_var_name


def test_to_var_name():
    test_cases = [
        ("us-east-1", "us_east_1"),
        ("arn:aws", "arn_aws"),
        ("a/b", "a__b"),
        ("database.table", "database_dot_table"),
    ]
    for before, after in test_cases:
        assert to_var_name(before) == after


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
