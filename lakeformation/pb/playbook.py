# -*- coding: utf-8 -*-

import json
import uuid
import boto3
from pathlib import Path
from colorama import Fore, Back, Style
from ordered_set import OrderedSet

from typing import (
    List, Tuple, Set, Dict, Iterable, Sequence, Mapping,
    Union, Any, Optional, Type,
)

from ..logger import logger
from ..abstract import HashableAbc
from ..principal import Principal
from ..permission import Permission
from ..resource import Resource, NonLfTagResource, LfTag
from ..validator import validate_attr_type
from ..utils import get_local_and_utc_now, get_diff_and_inter, grouper_list
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
        else:  # pragma: no cover
            self.workspace_dir: Path = Path(workspace_dir)

        if _skip_validation is False:  # pragma: no cover
            self.validate()

            self.glue_client = boto_ses.client("glue")
            self.lf_client = boto_ses.client("lakeformation")
            self.sts_client = boto_ses.client("sts")
            self.account_id: Optional[str] = self.sts_client.get_caller_identity()["Account"]
            self.region: Optional[str] = self.boto_ses.region_name
        else:
            self.account_id: Optional[str] = None
            self.region: Optional[str] = None

        self.deployed_pb: Optional[Playbook] = None

        self.resources: Dict[str, Resource] = dict()
        self.datalake_permissions: Dict[str, DataLakePermission] = dict()
        self.lf_tag_attachments: Dict[str, LfTagAttachment] = dict()

    @property
    def deployed_pb_json(self) -> Path:
        return Path(
            self.workspace_dir,
            f"deployed-{self.account_id}-{self.region}.json",
        )

    def validate(self):  # pragma: no cover
        validate_attr_type(self, "boto_ses", self.boto_ses, boto3.session.Session)
        assert self.workspace_dir.exists()

    def serialize(self) -> dict:
        local_now, utc_now = get_local_and_utc_now()
        try:
            username = Path.home().name
        except:  # pragma: no cover
            username = "unknown"
        data = {
            "deployed_by": username,
            "deployed_at_local_time": local_now.isoformat(),
            "deployed_at_utc_time": utc_now.isoformat(),
            "account_id": self.account_id,
            "region": self.region,
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
        """
        .. note::

            When you serialize, all LF tag instance are managed by playbook,
            When you deserialize, you should manually associate Lf tag instance
            with playbook

        :param data:
        :return:
        """
        pb = cls(_skip_validation=True)
        pb.account_id = data.get("account_id")
        pb.region = data.get("region")

        for id_, resource_dct in data.get("resources", dict()).items():
            pb.resources[id_] = Resource.deserialize(resource_dct)
            for res in pb.resources.values():
                if res.res_type == LfTag.res_type:
                    res.pb = pb

        for id_, dl_permission_dct in data.get("datalake_permissions", dict()).items():
            pb.datalake_permissions[id_] = DataLakePermission.deserialize(dl_permission_dct)
            for dl_permission in pb.datalake_permissions.values():
                res = dl_permission.resource
                if res.res_type == LfTag.res_type:
                    res.pb = pb

        for id_, lf_tag_attachment_dct in data.get("lf_tag_attachments", dict()).items():
            pb.lf_tag_attachments[id_] = LfTagAttachment.deserialize(lf_tag_attachment_dct)
            for lf_tag_attachment in pb.lf_tag_attachments.values():
                lf_tag_attachment.tag.pb = pb

        return pb

    def _add(
        self,
        obj: HashableAbc,
        collection: Dict[str, Any],
        type_: Type[HashableAbc],
    ):
        if not isinstance(obj, type_):  # pragma: no cover
            raise TypeError
        if obj.id in collection:  # pragma: no cover
            raise ValueError
        else:
            collection[obj.id] = obj

    def add_tag(self, lf_tag: LfTag):
        self._add(lf_tag, self.resources, LfTag)
        lf_tag.pb = self

    def add_dl_permission(self, dl_permission: DataLakePermission):
        self._add(dl_permission, self.datalake_permissions, DataLakePermission)
        if dl_permission.resource.res_type == LfTag.res_type:
            dl_permission.resource.pb = self

    def add_lf_tag_attachment(self, lf_tag_attachment: LfTagAttachment):
        self._add(lf_tag_attachment, self.lf_tag_attachments, LfTagAttachment)
        lf_tag_attachment.tag.pb = self

    def grant(
        self,
        principal: Principal,
        resource: Resource,
        permissions: List[Permission]
    ):
        for permission in permissions:
            dl_permission = DataLakePermission(
                principal=principal,
                resource=resource,
                permission=permission,
            )
            self.add_dl_permission(dl_permission)

    def attach(
        self,
        resource: NonLfTagResource,
        tag: LfTag,
    ):
        lf_tag_attachment = LfTagAttachment(
            resource=resource,
            tag=tag,
        )
        self.add_lf_tag_attachment(lf_tag_attachment)

    def load_deployed_playbook(self):
        """
        Load deployed LakeFormation object from the
        :attr:`Playbook.deployed_pb_json` file.

        If it is not exists, then initiate an empty :class:`Playbook` and
        serialize it to :attr:`Playbook.deployed_pb_json`` file
        """
        if self.deployed_pb_json.exists():
            self.deployed_pb = Playbook.deserialize(
                json.loads(self.deployed_pb_json.read_text())
            )
        else:
            self.deployed_pb = Playbook(_skip_validation=True)
            self.deployed_pb_json.write_text(
                json.dumps(self.deployed_pb.serialize(), indent=4)
            )

    @property
    def tags(self) -> Dict[str, 'LfTag']:
        return {
            res: res
            for res_id, res in self.resources.items()
            if res.res_type == LfTag.res_type
        }

    @property
    def tag_mapper(self) -> Dict[str, OrderedSet]:
        """
        Aggregate tag by key, and put values for the same key into a set.
        """
        mapper = dict()
        for tag_id, tag in self.tags.items():
            try:
                mapper[tag.key].add(tag.value)
            except KeyError:
                mapper[tag.key] = OrderedSet([tag.value, ])
        return mapper

    def apply(
        self,
        verbose=True,
        dry_run=False,
    ):  # pragma: no cover
        """

        :param verbose:
        :param dry_run:
        :return:
        **
        """
        self.load_deployed_playbook()
        self.apply_tags(verbose=verbose, dry_run=dry_run)
        self.apply_tag_attachment(verbose=verbose, dry_run=dry_run)
        self.apply_dl_permission(verbose=verbose, dry_run=dry_run)

        # pb = self.from
        if dry_run is False:
            self.deployed_pb_json.write_text(json.dumps(self.serialize(), indent=4))

    def apply_tags(
        self,
        verbose=True,
        dry_run=False,
    ):  # pragma: no cover
        """
        Ref:

        - Create: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.create_lf_tag
        - Update: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.update_lf_tag
        - Delete: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.delete_lf_tag
        """
        if not verbose:
            logger.enable_verbose = False

        new_tag_mapper, deployed_tag_mapper = self.tag_mapper, self.deployed_pb.tag_mapper
        (
            to_create_tag_id_set,
            to_delete_tag_id_set,
            to_update_tag_id_set,
        ) = get_diff_and_inter(new_tag_mapper, deployed_tag_mapper)

        to_create_tag_kwargs = [
            dict(
                CatalogId=self.account_id,
                TagKey=tag_key,
                TagValues=list(new_tag_mapper[tag_key]),
            )
            for tag_key in to_create_tag_id_set
        ]

        to_delete_tag_kwargs = [
            dict(
                CatalogId=self.account_id,
                TagKey=tag_key,
            )
            for tag_key in to_delete_tag_id_set
        ]

        to_update_tag_kwargs = list()
        for tag_key in to_update_tag_id_set:
            new_values = new_tag_mapper[tag_key]
            deployed_values = deployed_tag_mapper[tag_key]

            values_to_add = new_values.difference(deployed_values)
            values_to_delete = deployed_values.difference(new_values)

            kwargs = dict(
                CatalogId=self.account_id,
                TagKey=tag_key,
            )

            if len(values_to_add):
                kwargs["TagValuesToAdd"] = list(values_to_add)

            if len(values_to_delete):
                kwargs["TagValuesToDelete"] = list(values_to_delete)

            if len(values_to_add) >= 1 or len(values_to_delete) >= 1:
                to_update_tag_kwargs.append(kwargs)

        if len(to_create_tag_kwargs):
            msg = f"{Fore.CYAN}[Info] {Style.RESET_ALL}Create tags ..."
            logger.show(msg)

        for kwargs in to_create_tag_kwargs:
            msg = f"{Fore.GREEN}+ [Create Tag] {Style.RESET_ALL}{kwargs['TagKey']!r}"
            logger.show(msg)
            msg = f"- values: {kwargs['TagValues']!r}"
            logger.show(msg, indent=1)

            if dry_run is False:
                self.lf_client.create_lf_tag(**kwargs)

        if len(to_update_tag_kwargs):
            msg = f"{Fore.CYAN}[Info] {Style.RESET_ALL}Update tags ..."
            logger.show(msg)

        for kwargs in to_update_tag_kwargs:
            msg = f"{Fore.BLUE}~ [Update Tag] {Style.RESET_ALL}{kwargs['TagKey']!r}"
            logger.show(msg)

            if kwargs.get("TagValuesToAdd", list()):
                msg = f"{Fore.GREEN}+ values to add{Fore.RESET}: {kwargs['TagValuesToAdd']!r}"
                logger.show(msg, indent=1)

            if kwargs.get("TagValuesToDelete", list()):
                msg = f"{Fore.RED}- values to delete{Fore.RESET}: {kwargs['TagValuesToDelete']!r}"
                logger.show(msg, indent=1)

            if dry_run is False:
                self.lf_client.update_lf_tag(**kwargs)

        if len(to_delete_tag_kwargs):
            msg = f"{Fore.CYAN}[Info] {Style.RESET_ALL}Delete tags ..."
            logger.show(msg)

        for kwargs in to_delete_tag_kwargs:
            msg = f"{Fore.RED}- [Delete Tag] {Style.RESET_ALL}{kwargs['TagKey']!r}"
            logger.show(msg)
            if dry_run is False:
                self.lf_client.delete_lf_tag(**kwargs)

        logger.enable_verbose = True

    def apply_tag_attachment(
        self,
        verbose=True,
        dry_run=False,
    ):  # pragma: no cover
        """
        Ref:

        - Add: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.add_lf_tags_to_resource
        - Remove: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.remove_lf_tags_from_resource
        - Get: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lakeformation.html#LakeFormation.Client.get_resource_lf_tags
        """
        if not verbose:
            logger.enable_verbose = False

        new_attach_mapper = self.lf_tag_attachments
        deployed_attach_mapper = self.deployed_pb.lf_tag_attachments
        (
            to_add_attach_id_set,
            to_remove_attach_id_set,
            _,
        ) = get_diff_and_inter(new_attach_mapper, deployed_attach_mapper)

        to_add_kwargs_list: List[dict] = list()
        to_remove_kwargs_list: List[dict] = list()

        for attach_id in to_add_attach_id_set:
            attach = new_attach_mapper[attach_id]
            kwargs = dict(
                CatalogId=self.account_id,
                LFTags=[
                    dict(
                        CatalogId=self.account_id,
                        TagKey=attach.tag.key,
                        TagValues=[attach.tag.value, ],
                    )
                ]
            )
            kwargs["Resource"] = {
                attach.resource.get_add_remove_lf_tags_arg_name: \
                    attach.resource.get_add_remove_lf_tags_arg_value
            }
            to_add_kwargs_list.append(kwargs)

        for attach_id in to_remove_attach_id_set:
            attach = deployed_attach_mapper[attach_id]
            kwargs = dict(
                CatalogId=self.account_id,
                LFTags=[
                    dict(
                        CatalogId=self.account_id,
                        TagKey=attach.tag.key,
                        TagValues=[attach.tag.value, ],
                    )
                ]
            )
            kwargs["Resource"] = {
                attach.resource.get_add_remove_lf_tags_arg_name: \
                    attach.resource.get_add_remove_lf_tags_arg_value
            }
            to_remove_kwargs_list.append(kwargs)

        if len(to_add_kwargs_list):
            msg = f"{Fore.CYAN}[Info] {Style.RESET_ALL}Attach tags ..."
            logger.show(msg)

        for kwargs in to_add_kwargs_list:
            msg = f"{Fore.GREEN}+ [Attach Tag] {Style.RESET_ALL}{{{kwargs['LFTags'][0]['TagKey']!r}: {kwargs['LFTags'][0]['TagValues'][0]}}} to {kwargs['Resource']}"
            logger.show(msg)

            if dry_run is False:
                self.lf_client.add_lf_tags_to_resource(**kwargs)

        if len(to_remove_kwargs_list):
            msg = f"{Fore.CYAN}[Info] {Style.RESET_ALL}Detach tags ..."
            logger.show(msg)

        for kwargs in to_remove_kwargs_list:
            msg = f"{Fore.RED}- [Detach Tag] {Style.RESET_ALL}{{{kwargs['LFTags'][0]['TagKey']!r}: {kwargs['LFTags'][0]['TagValues'][0]}}} from {kwargs['Resource']}"
            logger.show(msg)

            if dry_run is False:
                self.lf_client.remove_lf_tags_from_resource(**kwargs)

        logger.enable_verbose = True

    def apply_dl_permission(
        self,
        verbose=True,
        dry_run=False,
    ):  # pragma: no cover
        """

        :param verbose:
        :param dry_run:
        :return:
        """
        if not verbose:
            logger.enable_verbose = False

        new_permit_mapper = self.datalake_permissions
        deployed_permit_mapper = self.deployed_pb.datalake_permissions

        (
            to_grant_permit_id_set,
            to_revoke_permit_id_set,
            _,
        ) = get_diff_and_inter(new_permit_mapper, deployed_permit_mapper)

        # we use batch grant / revoke API
        to_grant_entry_list: List[dict] = list()
        to_revoke_entry_list: List[dict] = list()

        # aggregate by principal and tag and resource type
        to_grant_permit_by_principal_and_tag_and_resource_type: Dict[str, List[DataLakePermission]] = dict()
        for permit_id in to_grant_permit_id_set:
            permit = new_permit_mapper[permit_id]
            key = f"{permit.principal.id}_{permit.resource.id}_{permit.permission.resource_type}"
            try:
                to_grant_permit_by_principal_and_tag_and_resource_type[key].append(permit)
            except KeyError:
                to_grant_permit_by_principal_and_tag_and_resource_type[key] = [permit, ]

        for _, permit_list in to_grant_permit_by_principal_and_tag_and_resource_type.items():
            permit = permit_list[0]
            entry = dict(
                Id=str(uuid.uuid4()),
                Principal=dict(
                    DataLakePrincipalIdentifier=permit.principal.id,
                ),
                Resource={
                    permit.resource.get_batch_grant_permission_arg_name: \
                        permit.resource.get_batch_grant_permission_arg_value(permit)
                },
            )
            permissions = [
                pa.permission.permission
                for pa in permit_list
                if pa.permission.grantable is False
            ]
            permissions_with_grant_option = [
                pa.permission.permission
                for pa in permit_list
                if pa.permission.grantable is True
            ]
            if len(permissions):
                entry["Permissions"] = permissions
            if len(permissions_with_grant_option):
                entry["PermissionsWithGrantOption"] = permissions_with_grant_option

            permissions_in_message = ", ".join([
                pa.permission.id
                for pa in permit_list
            ])
            msgs = [
                f"{Fore.GREEN}- [Grant Permission] {Style.RESET_ALL}{permit.principal.id} {permit.resource.id} {permissions_in_message}"
            ]
            entry["_msgs"] = msgs
            to_grant_entry_list.append(entry)

        # aggregate by principal and tag and resource type
        to_revoke_permit_by_principal_and_tag_and_resource_type: Dict[str, List[DataLakePermission]] = dict()
        for permit_id in to_revoke_permit_id_set:
            permit = deployed_permit_mapper[permit_id]
            key = f"{permit.principal.id}_{permit.resource.id}_{permit.permission.resource_type}"
            try:
                to_revoke_permit_by_principal_and_tag_and_resource_type[key].append(permit)
            except KeyError:
                to_revoke_permit_by_principal_and_tag_and_resource_type[key] = [permit, ]

        for _, permit_list in to_revoke_permit_by_principal_and_tag_and_resource_type.items():
            permit = permit_list[0]
            entry = dict(
                Id=str(uuid.uuid4()),
                Principal=dict(
                    DataLakePrincipalIdentifier=permit.principal.id,
                ),
                Resource={
                    permit.resource.get_batch_grant_permission_arg_name: \
                        permit.resource.get_batch_grant_permission_arg_value(permit)
                },
            )
            permissions = [
                pa.permission.permission
                for pa in permit_list
                if pa.permission.grantable is False
            ]
            permissions_with_grant_option = [
                pa.permission.permission
                for pa in permit_list
                if pa.permission.grantable is True
            ]
            if len(permissions):
                entry["Permissions"] = permissions
            if len(permissions_with_grant_option):
                entry["PermissionsWithGrantOption"] = permissions_with_grant_option

            permissions_in_message = ", ".join([
                pa.permission.id
                for pa in permit_list
            ])
            msgs = [
                f"{Fore.RED}- [Revoke Permission] {Style.RESET_ALL}{permit.principal.id} {permit.resource.id} {permissions_in_message}"
            ]
            entry["_msgs"] = msgs
            to_revoke_entry_list.append(entry)

        if len(to_grant_entry_list):
            msg = f"{Fore.CYAN}[Info] {Style.RESET_ALL}Grant permissions ..."
            logger.show(msg)

        for to_grant_entry_sub_list in grouper_list(to_grant_entry_list, 20):
            for entry in to_grant_entry_sub_list:
                msgs = entry.pop("_msgs")
                for msg in msgs:
                    logger.show(msg)

            if dry_run is False:
                self.lf_client.batch_grant_permissions(
                    CatalogId=self.account_id,
                    Entries=to_grant_entry_sub_list
                )

        if len(to_revoke_entry_list):
            msg = f"{Fore.CYAN}[Info] {Style.RESET_ALL}Revoke permissions ..."
            logger.show(msg)

        for to_revoke_entry_sub_list in grouper_list(to_revoke_entry_list, 20):
            for entry in to_revoke_entry_sub_list:
                msgs = entry.pop("_msgs")
                for msg in msgs:
                    logger.show(msg)

            if dry_run is False:
                self.lf_client.batch_revoke_permissions(
                    CatalogId=self.account_id,
                    Entries=to_revoke_entry_sub_list
                )

        logger.enable_verbose = True
