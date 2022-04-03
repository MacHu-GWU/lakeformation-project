# -*- coding: utf-8 -*-

"""
Exception definition
"""

from typing import Type


class ValidationError(Exception):
    @classmethod
    def from_validate_attr_type(
        cls,
        inst,
        attr: str,
        value,
        tp: Type,
    ) -> 'ValidationError':
        msg = f"{inst.__class__.__name__}.{attr} = {value!r} is NOT {tp} type!"
        return cls(msg)
