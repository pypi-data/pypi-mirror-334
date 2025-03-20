from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

import datetime
from ..models.get_drive_labels_properties import GetDriveLabelsProperties
from ..models.get_drive_labels_lifecycle import GetDriveLabelsLifecycle
from ..models.get_drive_labels_applied_label_policy import (
    GetDriveLabelsAppliedLabelPolicy,
)
from ..models.get_drive_labels_publisher import GetDriveLabelsPublisher
from ..models.get_drive_labels_display_hints import GetDriveLabelsDisplayHints
from ..models.get_drive_labels_fields_array_item_ref import (
    GetDriveLabelsFieldsArrayItemRef,
)
from ..models.get_drive_labels_applied_capabilities import (
    GetDriveLabelsAppliedCapabilities,
)
from ..models.get_drive_labels_creator import GetDriveLabelsCreator
from ..models.get_drive_labels_revision_creator import GetDriveLabelsRevisionCreator


class GetDriveLabels(BaseModel):
    """
    Attributes:
        creator (Optional[GetDriveLabelsCreator]):
        fields (Optional[list['GetDriveLabelsFieldsArrayItemRef']]):
        applied_capabilities (Optional[GetDriveLabelsAppliedCapabilities]):
        label_type (Optional[str]): The Label type Example: ADMIN.
        id (Optional[str]): The ID Example: QbB2rdw2uwJokXviXMZSjYwsiFZCsy5yJJ1RNNEbbFcb.
        publish_time (Optional[datetime.datetime]): The Publish time Example: 2023-10-27T10:25:07.7005810+00:00.
        revision_creator (Optional[GetDriveLabelsRevisionCreator]):
        learn_more_uri (Optional[str]): The Learn more uri Example: https://learnmorelink.com.
        name (Optional[str]): The Name Example: labels/QbB2rdw2uwJokXviXMZSjYwsiFZCsy5yJJ1RNNEbbFcb@42.
        publisher (Optional[GetDriveLabelsPublisher]):
        lifecycle (Optional[GetDriveLabelsLifecycle]):
        display_hints (Optional[GetDriveLabelsDisplayHints]):
        properties (Optional[GetDriveLabelsProperties]):
        applied_label_policy (Optional[GetDriveLabelsAppliedLabelPolicy]):
        revision_create_time (Optional[datetime.datetime]): The Revision create time Example:
            2023-10-27T10:25:07.7005810+00:00.
        revision_id (Optional[str]): The Revision ID Example: 42.
        create_time (Optional[datetime.datetime]): The Create time Example: 2023-06-14T09:34:23.2178300+00:00.
        customer (Optional[str]): The Customer Example: customers/C01iikpby.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    creator: Optional["GetDriveLabelsCreator"] = Field(alias="creator", default=None)
    fields: Optional[list["GetDriveLabelsFieldsArrayItemRef"]] = Field(
        alias="fields", default=None
    )
    applied_capabilities: Optional["GetDriveLabelsAppliedCapabilities"] = Field(
        alias="appliedCapabilities", default=None
    )
    label_type: Optional[str] = Field(alias="labelType", default=None)
    id: Optional[str] = Field(alias="id", default=None)
    publish_time: Optional[datetime.datetime] = Field(alias="publishTime", default=None)
    revision_creator: Optional["GetDriveLabelsRevisionCreator"] = Field(
        alias="revisionCreator", default=None
    )
    learn_more_uri: Optional[str] = Field(alias="learnMoreUri", default=None)
    name: Optional[str] = Field(alias="name", default=None)
    publisher: Optional["GetDriveLabelsPublisher"] = Field(
        alias="publisher", default=None
    )
    lifecycle: Optional["GetDriveLabelsLifecycle"] = Field(
        alias="lifecycle", default=None
    )
    display_hints: Optional["GetDriveLabelsDisplayHints"] = Field(
        alias="displayHints", default=None
    )
    properties: Optional["GetDriveLabelsProperties"] = Field(
        alias="properties", default=None
    )
    applied_label_policy: Optional["GetDriveLabelsAppliedLabelPolicy"] = Field(
        alias="appliedLabelPolicy", default=None
    )
    revision_create_time: Optional[datetime.datetime] = Field(
        alias="revisionCreateTime", default=None
    )
    revision_id: Optional[str] = Field(alias="revisionId", default=None)
    create_time: Optional[datetime.datetime] = Field(alias="createTime", default=None)
    customer: Optional[str] = Field(alias="customer", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(cls: Type["GetDriveLabels"], src_dict: Dict[str, Any]):
        return cls.model_validate(src_dict)

    @property
    def additional_keys(self) -> list[str]:
        base_fields = self.model_fields.keys()
        return [k for k in self.__dict__ if k not in base_fields]

    def __getitem__(self, key: str) -> Any:
        if key in self.__dict__:
            return self.__dict__[key]
        raise KeyError(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.__dict__[key] = value

    def __delitem__(self, key: str) -> None:
        if key in self.__dict__:
            del self.__dict__[key]
        else:
            raise KeyError(key)

    def __contains__(self, key: str) -> bool:
        return key in self.__dict__
