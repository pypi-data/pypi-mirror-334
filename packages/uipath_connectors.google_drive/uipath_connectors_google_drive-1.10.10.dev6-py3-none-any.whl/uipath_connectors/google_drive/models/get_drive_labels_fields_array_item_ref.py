from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Optional, Type

from ..models.get_drive_labels_fields_properties import GetDriveLabelsFieldsProperties
from ..models.get_drive_labels_fields_updater import GetDriveLabelsFieldsUpdater
from ..models.get_drive_labels_fields_creator import GetDriveLabelsFieldsCreator
from ..models.get_drive_labels_fields_publisher import GetDriveLabelsFieldsPublisher
from ..models.get_drive_labels_fields_lifecycle import GetDriveLabelsFieldsLifecycle
from ..models.get_drive_labels_fields_display_hints import (
    GetDriveLabelsFieldsDisplayHints,
)
from ..models.get_drive_labels_fields_applied_capabilities import (
    GetDriveLabelsFieldsAppliedCapabilities,
)
from ..models.get_drive_labels_fields_selection_options import (
    GetDriveLabelsFieldsSelectionOptions,
)


class GetDriveLabelsFieldsArrayItemRef(BaseModel):
    """
    Attributes:
        publisher (Optional[GetDriveLabelsFieldsPublisher]):
        selection_options (Optional[GetDriveLabelsFieldsSelectionOptions]):
        applied_capabilities (Optional[GetDriveLabelsFieldsAppliedCapabilities]):
        query_key (Optional[str]): The Fields query key Example:
            labels/QbB2rdw2uwJokXviXMZSjYwsiFZCsy5yJJ1RNNEbbFcb.8328BA9DE8.
        display_hints (Optional[GetDriveLabelsFieldsDisplayHints]):
        updater (Optional[GetDriveLabelsFieldsUpdater]):
        creator (Optional[GetDriveLabelsFieldsCreator]):
        lifecycle (Optional[GetDriveLabelsFieldsLifecycle]):
        properties (Optional[GetDriveLabelsFieldsProperties]):
        id (Optional[str]): The Fields ID Example: 8328BA9DE8.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    publisher: Optional["GetDriveLabelsFieldsPublisher"] = Field(
        alias="publisher", default=None
    )
    selection_options: Optional["GetDriveLabelsFieldsSelectionOptions"] = Field(
        alias="selectionOptions", default=None
    )
    applied_capabilities: Optional["GetDriveLabelsFieldsAppliedCapabilities"] = Field(
        alias="appliedCapabilities", default=None
    )
    query_key: Optional[str] = Field(alias="queryKey", default=None)
    display_hints: Optional["GetDriveLabelsFieldsDisplayHints"] = Field(
        alias="displayHints", default=None
    )
    updater: Optional["GetDriveLabelsFieldsUpdater"] = Field(
        alias="updater", default=None
    )
    creator: Optional["GetDriveLabelsFieldsCreator"] = Field(
        alias="creator", default=None
    )
    lifecycle: Optional["GetDriveLabelsFieldsLifecycle"] = Field(
        alias="lifecycle", default=None
    )
    properties: Optional["GetDriveLabelsFieldsProperties"] = Field(
        alias="properties", default=None
    )
    id: Optional[str] = Field(alias="id", default=None)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True, by_alias=True)

    @classmethod
    def from_dict(
        cls: Type["GetDriveLabelsFieldsArrayItemRef"], src_dict: Dict[str, Any]
    ):
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
