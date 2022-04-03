# -*- coding: utf-8 -*-

from typing import Type

from .exc import ValidationError


def validate_attr_type(
    inst,
    attr: str,
    value,
    tp: Type,
):
    if not isinstance(value, tp):
        raise ValidationError.from_validate_attr_type(inst, attr, value, tp)
