# -*- coding: utf-8 -*-

"""

"""

import pytest

import boto3
from pathlib import Path
from lakeformation import gen_resource, gen_principal
from lakeformation.runtime import IS_CI

dir_here = Path(__file__).absolute().parent


def setup_module(module):
    for p in dir_here.iterdir():
        if p.name.startswith("resource_") and p.name.endswith(".py"):
            p.unlink(missing_ok=True)
        if p.name.startswith("principal_") and p.name.endswith(".py"):
            p.unlink(missing_ok=True)


def test_gen_code():
    if IS_CI:
        return
    
    profile_name = None
    region_name = "us-east-1"
    boto_ses = boto3.session.Session(profile_name=profile_name, region_name=region_name)

    gen_resource(boto_ses=boto_ses, workspace_dir=str(dir_here))
    gen_principal(boto_ses=boto_ses, workspace_dir=str(dir_here))


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
