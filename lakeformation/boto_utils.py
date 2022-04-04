# -*- coding: utf-8 -*-

from typing import Callable, List


def list_recursively(
    method: Callable,
    default_kwargs: dict,
    next_token_arg_name: str,
    next_token_value_field: str,
    collection_value_field: str,
):
    """
    Given an paginator API like this::

        response = client.get_databases(
            CatalogId='string',
            NextToken='string',
            MaxResults=123,
            ResourceShareType='FOREIGN'|'ALL'
        )

    Response schema like this::

        {
            'DatabaseList': [
                {},
                {},
                ...
            ],
            'NextToken': 'string'
        }

    This api will retrieve the database list recursively in one api call::

        list_recursively(
            method=client.get_database,
            default_kwargs=dict(
                CatalogId="111122223333",
                MaxResults=1,
                ResourceShareType="ALL",
            ),
            next_token_arg_name="NextToken",
            next_token_value_field="NextToken",
            collection_value_field="DatabaseList",
        )

    :param method:
    :param default_kwargs:
    :param next_token_arg_name:
    :param next_token_value_field:
    :param collection_value_field:
    :return:
    """
    next_token = None
    lst: List[dict] = list()
    while 1:
        kwargs = default_kwargs.copy()
        if next_token is not None:
            kwargs[next_token_arg_name] = next_token
        response = method(**kwargs)
        next_token = response.get(next_token_value_field)
        lst.extend(response.get(collection_value_field, list()))
        if next_token is None:
            break
    return lst
