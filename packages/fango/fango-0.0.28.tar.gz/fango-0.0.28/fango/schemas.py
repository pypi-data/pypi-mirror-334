from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from types import UnionType
from typing import Any, Generic, TypedDict, TypeVar, get_args
from uuid import UUID

from django.db.models import IntegerChoices, Manager, TextChoices
from pydantic import BaseModel, ConfigDict, field_validator, model_validator
from pydantic_core.core_schema import FieldValidationInfo
from typing_extensions import NotRequired

from fango.adapters.types import PK
from fango.generics import BaseModelT

__all__ = [
    "Cursor",
    "Page",
    "Entry",
    "ChoicesItem",
    "FangoModel",
    "ActionClasses",
    "Multiselect",
    "CRUDAdapter",
    "AURAdapter",
    "DBModel",
]

T = TypeVar("T")


@dataclass
class Cursor:
    offset: int
    reverse: int
    position: str | None


class Page(BaseModel, Generic[T]):
    """
    Adapter for view paginated data.

    """

    next: str | None = None
    previous: str | None = None
    results: list[T]


class CRUDAdapter(BaseModel, Generic[T]):
    """
    Adapter for wrap CRUD relations in schema:

    CR - Create
    U - Update
    D - Delete

    """

    create: list[T] = []
    update: list[T] = []
    delete: list[PK]


class AURAdapter(BaseModel, Generic[T]):
    """
    Adapter for wrap AUR relations in schema:

    A - Add
    U - Update
    R - Remove

    """

    add: list[PK] = []
    update: list[T] = []
    remove: list[PK]


class Entry(BaseModel, Generic[T]):
    """
    Adapter for view entry data with page meta fields.

    """

    title: str | None = None
    status: str | None = None
    results: T


class ChoicesItem(BaseModel, Generic[T]):
    """
    Adapter for view choices item as multiselect item.

    """

    id: T
    name: str | None


class FangoModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        json_encoders={Decimal: lambda v: v.normalize()},
    )

    @field_validator("*", mode="before")
    def model_manager(cls, value: Any, info: FieldValidationInfo):
        if isinstance(value, Manager) and info.field_name:
            annotations = get_args(cls.model_fields[info.field_name].annotation)

            if any(type in annotations for type in [PK, list[PK], int, list[int], UUID, list[UUID]]):
                return value.values_list("pk", flat=True)
            else:
                return value.all()

        return value

    @model_validator(mode="before")
    @classmethod
    def choices_label(cls, data):
        from fango.utils import get_choices_label

        for key, field in cls.model_fields.items():
            value = data.get(key, field.default) if isinstance(data, dict) else getattr(data, key, field.default)
            for arg in get_args(field.annotation):
                if not isinstance(arg, UnionType):
                    if issubclass(arg, IntegerChoices) or issubclass(arg, TextChoices):
                        label = get_choices_label(arg, value)
                        data.update({key: label}) if isinstance(data, dict) else setattr(data, key, label)

                    elif issubclass(arg, Enum):
                        data.update({key: label}) if isinstance(data, dict) else setattr(data, key, label)

                    elif metadata := getattr(arg, "__pydantic_generic_metadata__", None):
                        if metadata["origin"] is ChoicesItem and value is not None:
                            if isinstance(value, ChoicesItem):
                                label = value.name
                                value = value.id.value
                            else:
                                label = get_choices_label(metadata["args"][0], value)
                            (
                                data.update({key: {"id": value, "name": label}})
                                if isinstance(data, dict)
                                else setattr(data, key, {"id": value, "name": label})
                            )
        return data


class Multiselect(FangoModel):
    id: int
    name: str | None = None


class DBModel(BaseModel):
    """
    NOTE: неочевидный момент - если используется в crud адаптере,
          НЕОБХОДИМО назначать поле id. В обратном случае - его строго не должно быть

    """

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class ActionClasses(TypedDict, Generic[BaseModelT]):
    list: NotRequired[BaseModelT]
    retrieve: NotRequired[BaseModelT]
    update: NotRequired[BaseModelT]
    delete: NotRequired[BaseModelT]
    page_meta: NotRequired[BaseModelT]


class Token(BaseModel):
    access: str


class OpenAPIToken(BaseModel):
    access_token: str
    token_type: str


class Credentials(BaseModel):
    email: str
    password: str
