# -*- coding: utf-8 -*-

from lakeformation import Database, Table, Column

{% for database in database_list %}
{{ database.render_define() }}

{% for table in database.t.values() %}
{{ table.render_define() }}

{% for column in table.c.values() %}
{{ column.render_define() }}
{% endfor %}

{% endfor %}

{% endfor %}
