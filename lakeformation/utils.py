# -*- coding: utf-8 -*-

var_name_escape = {
    "-": "_",
    ":": "_",
    "/": "__",
    ".": "_dot_",
}


def to_var_name(s: str) -> str:
    """
    Convert string to variable name safe format. For example::

        >>> to_var_name("us-east-1")
        us_east_1
        >>> to_var_name("arn:aws")
        arn_aws
        >>> to_var_name("a/b")
        a__b
        >>> to_var_name("database.table")
        database_dot_table
    """
    for k, v in var_name_escape.items():
        s = s.replace(k, v)
    return s
