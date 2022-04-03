# -*- coding: utf-8 -*-

import pytest
from lakeformation.validator import validate_attr_type, ValidationError


class BankAccount:
    def __init__(self, acc_id: str, balance: int):
        self.acc_id = acc_id
        self.balance = balance
        self.validate()

    def validate(self):
        validate_attr_type(self, "acc_id", self.acc_id, str)
        validate_attr_type(self, "balance", self.balance, int)


def test_validate_attr_type():
    with pytest.raises(ValidationError):
        _ = BankAccount(acc_id=0, balance=0)

    with pytest.raises(ValidationError):
        _ = BankAccount(acc_id="a", balance="a")

    _ = BankAccount(acc_id="a", balance=0)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
