# -*- coding: utf-8 -*-

import boto3
from pathlib import Path

from typing import (
    List, Tuple, Set, Dict, Iterable, Sequence, Mapping,
    Union, Any, Optional, Type,
)

from ..abstract import HashableAbc
from ..principal import Principal
from ..permission import Permission
from ..resource import Resource, LfTag
from ..validator import validate_attr_type
from ..utils import get_local_and_utc_now
from .asso import DataLakePermission, LfTagAttachment


class Playbook:
    def __init__(
        self,
        boto_ses: boto3.session.Session = None,
        workspace_dir: str = None,
        _skip_validation: bool = False
    ):
        self.boto_ses = boto_ses
        if workspace_dir is None:
            self.workspace_dir: Path = Path.cwd()
        else:
            self.workspace_dir: Path = Path(self.workspace_dir)

        if not _skip_validation:
            self.validate()

            self.glue_client = boto_ses.client("glue")
            self.lf_client = boto_ses.client("lakeformation")
            self.sts_client = boto_ses.client("sts")
            self.region: str = self.boto_ses.region_name
            self.account_id: str = self.sts_client.get_caller_identity()["Account"]

            self.deployed_json: Path = Path(
                self.workspace_dir,
                f"deployed-{self.account_id}-{self.region}.json",
            )

        self.deployed_pb: Optional[Playbook] = None

        self.resources: Dict[str, Resource] = dict()
        self.datalake_permissions: Dict[str, DataLakePermission] = dict()
        self.lf_tag_attachments: Dict[str, LfTagAttachment] = dict()

    def validate(self):
        validate_attr_type(self, "boto_ses", self.boto_ses, boto3.session.Session)
        assert self.workspace_dir.exists()

    def serialize(self) -> dict:
        local_now, utc_now = get_local_and_utc_now()
        try:
            username = Path.home().name
        except:
            username = "unknown"
        data = {
            "deployed_by": username,
            "deployed_at_local_time": local_now.isoformat(),
            "deployed_at_utc_time": utc_now.isoformat(),
            "resources": {
                id_: res.serialize()
                for id_, res in self.resources.items()
            },
            "datalake_permissions": {
                id_: dl_permission.serialize()
                for id_, dl_permission in self.datalake_permissions.items()
            },
            "lf_tag_attachments": {
                id_: lf_tag_attachment.serialize()
                for id_, lf_tag_attachment in self.lf_tag_attachments.items()
            },
        }
        return data

    @classmethod
    def deserialize(cls, data: dict) -> 'Playbook':
        pb = cls(_skip_validation=True)
        for id_, resource_dct in data.get("resources", dict()).items():
            pb.resources[id_] = Resource.deserialize(resource_dct)
        for id_, dl_permission_dct in data.get("datalake_permissions", dict()).items():
            pb.datalake_permissions[id_] = DataLakePermission.deserialize(dl_permission_dct)
        for id_, lf_tag_attachment_dct in data.get("lf_tag_attachments", dict()).items():
            pb.lf_tag_attachments[id_] = LfTagAttachment.deserialize(lf_tag_attachment_dct)
        return pb

    def _add(
        self,
        obj: HashableAbc,
        collection: Dict[str, Any],
        type_: Type[HashableAbc],
    ):
        if not isinstance(obj, type_):
            raise TypeError
        if obj.id in collection:
            raise ValueError
        else:
            collection[obj.id] = obj

    def add_tag(self, lf_tag: LfTag):
        self._add(lf_tag, self.resources, LfTag)

    def add_dl_permission(self, dl_permission: DataLakePermission):
        self._add(dl_permission, self.datalake_permissions, DataLakePermission)

    def add_tag_attachment(self, lf_tag_attachment: LfTagAttachment):
        self._add(lf_tag_attachment, self.lf_tag_attachments, LfTagAttachment)
