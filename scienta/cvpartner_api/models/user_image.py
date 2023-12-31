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
from pydantic import BaseModel, StrictStr
from scienta.cvpartner_api.models.image_url import ImageUrl
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class UserImage(BaseModel):
    """
    UserImage
    """ # noqa: E501
    url: Optional[StrictStr] = None
    thumb: Optional[ImageUrl] = None
    fit_thumb: Optional[ImageUrl] = None
    large: Optional[ImageUrl] = None
    small_thumb: Optional[ImageUrl] = None
    __properties: ClassVar[List[str]] = ["url", "thumb", "fit_thumb", "large", "small_thumb"]

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
        """Create an instance of UserImage from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of thumb
        if self.thumb:
            _dict['thumb'] = self.thumb.to_dict()
        # override the default output from pydantic by calling `to_dict()` of fit_thumb
        if self.fit_thumb:
            _dict['fit_thumb'] = self.fit_thumb.to_dict()
        # override the default output from pydantic by calling `to_dict()` of large
        if self.large:
            _dict['large'] = self.large.to_dict()
        # override the default output from pydantic by calling `to_dict()` of small_thumb
        if self.small_thumb:
            _dict['small_thumb'] = self.small_thumb.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of UserImage from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "url": obj.get("url"),
            "thumb": ImageUrl.from_dict(obj.get("thumb")) if obj.get("thumb") is not None else None,
            "fit_thumb": ImageUrl.from_dict(obj.get("fit_thumb")) if obj.get("fit_thumb") is not None else None,
            "large": ImageUrl.from_dict(obj.get("large")) if obj.get("large") is not None else None,
            "small_thumb": ImageUrl.from_dict(obj.get("small_thumb")) if obj.get("small_thumb") is not None else None
        })
        return _obj

