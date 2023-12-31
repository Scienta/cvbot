# coding: utf-8

"""
    CVPartner

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.0.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Any, ClassVar, Dict, List, Optional
from pydantic import BaseModel, StrictBool, StrictInt, StrictStr
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class KeyQualification(BaseModel):
    """
    KeyQualification
    """ # noqa: E501
    order: Optional[StrictInt] = None
    starred: Optional[StrictBool] = None
    disabled: Optional[StrictBool] = None
    version: Optional[StrictInt] = None
    external_unique_id: Optional[StrictStr] = None
    owner_updated_at: Optional[StrictStr] = None
    created_at: Optional[StrictStr] = None
    updated_at: Optional[StrictStr] = None
    recently_added: Optional[StrictBool] = None
    label: Optional[Dict[str, Any]] = None
    long_description: Optional[Dict[str, Any]] = None
    tag_line: Optional[Dict[str, Any]] = None
    __properties: ClassVar[List[str]] = ["order", "starred", "disabled", "version", "external_unique_id", "owner_updated_at", "created_at", "updated_at", "recently_added", "label", "long_description", "tag_line"]

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True
    }


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of KeyQualification from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        _dict = self.model_dump(
            by_alias=True,
            exclude={
            },
            exclude_none=True,
        )
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of KeyQualification from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "order": obj.get("order"),
            "starred": obj.get("starred"),
            "disabled": obj.get("disabled"),
            "version": obj.get("version"),
            "external_unique_id": obj.get("external_unique_id"),
            "owner_updated_at": obj.get("owner_updated_at"),
            "created_at": obj.get("created_at"),
            "updated_at": obj.get("updated_at"),
            "recently_added": obj.get("recently_added"),
            "label": obj.get("label"),
            "long_description": obj.get("long_description"),
            "tag_line": obj.get("tag_line")
        })
        return _obj

