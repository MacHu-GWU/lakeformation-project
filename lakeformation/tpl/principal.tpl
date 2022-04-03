# -*- coding: utf-8 -*-

from lakeformation import IamUser, IamRole, IamGroup

{% for iam_role in iam_role_list %}
{{ iam_role.render() }}
{% endfor %}

{% for iam_user in iam_user_list %}
{{ iam_user.render() }}
{% endfor %}

{% for iam_group in iam_group_list %}
{{ iam_group.render() }}
{% endfor %}
