# -*- coding: utf-8 -*-

import pytest
from pathlib import Path
from lakeformation.pb.playbook import (
    Playbook, DataLakePermission, LfTagAttachment,
)
from lakeformation.resource import (
    DataLakeLocation, DataCellsFilter, LfTag,
)
from lakeformation.permission import PermissionEnum
from lakeformation.tests import Objects, aws_account_id, aws_region

dir_here = Path(__file__).absolute().parent


def setup_module(module):
    for p in dir_here.iterdir():
        if p.name.startswith("deployed_") and p.name.endswith(".json"):
            p.unlink(missing_ok=True)


class TestPlaybook:
    def test_resource_init_with_playbook(self):
        pb = Playbook(_skip_validation=True)

        tag = LfTag(catalog_id="111122223333", key="admin", value="y")
        assert tag.playbook_managed is False

        tag = LfTag(catalog_id="111122223333", key="admin", value="y", pb=pb)
        assert tag.playbook_managed is True

        loc = DataLakeLocation(catalog_id="111122223333", resource_arn="s3://my-bucket")
        assert loc.playbook_managed is False

        loc = DataLakeLocation(catalog_id="111122223333", resource_arn="s3://my-bucket", pb=pb)
        assert loc.playbook_managed is True

        ft = DataCellsFilter(
            filter_name="my_filter",
            catalog_id="111122223333",
            database_name="db", table_name="tb",
            row_filter_expression="name='alice'",
            include_columns=["name",]
        )
        assert ft.playbook_managed is False

        ft = DataCellsFilter(
            filter_name="my_filter",
            catalog_id="111122223333",
            database_name="db", table_name="tb",
            row_filter_expression="name='alice'",
            include_columns=["name",],
            pb=pb,
        )
        assert ft.playbook_managed is True

        with pytest.raises(ValueError):
            pb.add_tag(tag)

        with pytest.raises(ValueError):
            pb.add_dl_location(loc)

        with pytest.raises(ValueError):
            pb.add_data_filter(ft)

    def test_seder(self):
        obj = Objects()

        pb = Playbook(_skip_validation=True)
        pb.account_id = aws_account_id
        pb.region = aws_region

        pb.add_tag(obj.tag_admin_y)
        pb.add_tag(obj.tag_admin_n)

        pb.attach(obj.db_amz, obj.tag_admin_y)

        pb.grant(obj.iam_user_alice, obj.tag_admin_y,
                 [PermissionEnum.SuperDatabase.value, PermissionEnum.SuperTable.value])

        pb.load_deployed_playbook()  # test the logic when it not exists
        pb.load_deployed_playbook()  # test the logic when it exists

        pb1 = Playbook.deserialize(pb.serialize())
        assert pb.account_id == pb1.account_id
        assert pb.region == pb1.region
        assert pb.region == pb1.region
        assert pb.region == pb1.region
        assert pb.region == pb1.region

        assert len(pb.tag_mapper) == 1

        _ = obj.db_amz.get_add_remove_lf_tags_arg_name
        _ = obj.db_amz.get_add_remove_lf_tags_arg_value
        _ = obj.tb_amz_user.get_add_remove_lf_tags_arg_name
        _ = obj.tb_amz_user.get_add_remove_lf_tags_arg_value
        _ = obj.col_amz_user_password.get_add_remove_lf_tags_arg_name
        _ = obj.col_amz_user_password.get_add_remove_lf_tags_arg_value

        _ = obj.tag_admin_y.batch_grant_remove_permission_arg_name
        _ = obj.tag_admin_y.batch_grant_remove_permission_arg_value(
            dl_permission=list(pb.datalake_permissions.values())[0]
        )


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
