# -*- coding: utf-8 -*-

from lakeformation import Database, Table, Column

{% for database in database_list %}
{{ database.render() }}

{% for table in database.t.values() %}
{{ table.render() }}

{% for column in table.c.values() %}
{{ column.render() }}
{% endfor %}

{% endfor %}

{% endfor %}
