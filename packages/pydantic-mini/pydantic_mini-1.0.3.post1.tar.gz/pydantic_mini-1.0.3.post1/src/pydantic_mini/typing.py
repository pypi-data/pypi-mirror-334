from __future__ import annotations

import inspect
import re
import sys
import types
import typing
import collections
from dataclasses import MISSING, Field, InitVar

if sys.version_info < (3, 9):
    from typing_extensions import Annotated, get_origin, get_args
else:
    from typing import Annotated, get_origin, get_args

from .exceptions import ValidationError

if typing.TYPE_CHECKING:
    from .base import BaseModel

__all__ = (
    "Annotated",
    "MiniAnnotated",
    "Attrib",
    "get_type",
    "is_collection",
    "is_optional_type",
    "is_type",
    "is_mini_annotated",
    "NoneType",
    "ModelConfig",
    "DEFAULT_MODEL_CONFIG",
    "is_builtin_type",
    "InitVar",
    "is_initvar_type",
    "is_class_var_type",
)


# backward compatibility
NoneType = getattr(types, "NoneType", type(None))


class ModelConfig(typing.TypedDict, total=False):
    init: bool
    repr: bool
    eq: bool
    order: bool
    unsafe_hash: bool
    frozen: bool


DEFAULT_MODEL_CONFIG = ModelConfig(
    init=True,
    repr=True,
    eq=True,
    order=False,
    unsafe_hash=False,
    frozen=False,
)


class Attrib:
    __slots__ = (
        "default",
        "default_factory",
        "required",
        "gt",
        "ge",
        "lt",
        "le",
        "min_length",
        "max_length",
        "pattern",
        "_validators",
    )

    def __init__(
        self,
        default: typing.Optional[typing.Any] = MISSING,
        default_factory: typing.Optional[typing.Callable[[], typing.Any]] = MISSING,
        required: bool = False,
        gt: typing.Optional[float] = None,
        ge: typing.Optional[float] = None,
        lt: typing.Optional[float] = None,
        le: typing.Optional[float] = None,
        min_length: typing.Optional[int] = None,
        max_length: typing.Optional[int] = None,
        pattern: typing.Optional[typing.Union[str, typing.Pattern]] = None,
        validators: typing.Optional[
            typing.List[typing.Callable[[typing.Any], typing.Any]]
        ] = MISSING,
    ):
        self.default = default
        self.default_factory = default_factory
        self.required = required
        self.gt = gt
        self.ge = ge
        self.lt = lt
        self.le = le
        self.min_length = min_length
        self.max_length = max_length
        self.pattern = pattern

        if validators is not MISSING:
            self._validators = (
                validators if isinstance(validators, (list, tuple)) else [validators]
            )
        else:
            self._validators = []

    def __repr__(self):
        return (
            "Query("
            f"default={self.default!r},"
            f"default_factory={self.default_factory!r},"
            ")"
        )

    def has_default(self):
        return self.default is not MISSING or self.default_factory is not MISSING

    def _get_default(self) -> typing.Any:
        if self.default is not MISSING:
            return self.default
        elif self.default_factory is not MISSING:
            return self.default_factory()

    def validate(self, value: typing.Any, field_name: str) -> typing.Optional[bool]:
        value = value or self._get_default()

        if self.required and value is None:
            raise ValidationError(
                f"Field '{field_name}' is required but not provided (value is None).",
                params={"field_name": field_name},
            )

        for name in ("gt", "ge", "lt", "le", "min_length", "max_length", "pattern"):
            validation_factor = getattr(self, name, None)

            # Skip the validation if 'validation_factor' is None, or if both 'value'
            # and 'self.default' are None
            if validation_factor is None or (value is None and self.default is None):
                continue

            validator = getattr(self, f"_validate_{name}")
            validator(value)
        return True

    def execute_field_validators(self, instance: "BaseModel", fd: Field) -> None:
        for validator in self._validators:
            try:
                result = validator(instance, getattr(instance, fd.name))
                if result is not None:
                    setattr(instance, fd.name, result)
            except Exception as e:
                if isinstance(e, ValidationError):
                    raise
                raise ValidationError(str(e)) from e

    def _validate_gt(self, value: typing.Any):
        try:
            if not (value > self.gt):
                raise ValidationError(
                    f"Field value '{value}' is not greater than '{self.gt}'",
                    params={"gt": self.gt},
                )
        except TypeError:
            raise TypeError(
                f"Unable to apply constraint 'gt' to supplied value {value!r}"
            )

    def _validate_ge(self, value: typing.Any):
        try:
            if not (value >= self.ge):
                raise ValidationError(
                    f"Field value '{value}' is not greater than or equal to '{self.ge}'",
                    params={"ge": self.ge},
                )
        except TypeError:
            raise TypeError(
                f"Unable to apply constraint 'ge' to supplied value {value!r}"
            )

    def _validate_lt(self, value: typing.Any):
        try:
            if not (value < self.lt):
                raise ValidationError(
                    f"Field value '{value}' is not less than '{self.lt}'",
                    params={"lt": self.lt},
                )
        except TypeError:
            raise TypeError(
                f"Unable to apply constraint 'lt' to supplied value {value!r}"
            )

    def _validate_le(self, value: typing.Any):
        try:
            if not (value <= self.le):
                raise ValidationError(
                    f"Field value '{value}' is not less than or equal to '{self.le}'",
                    params={"le": self.le},
                )
        except TypeError:
            raise TypeError(
                f"Unable to apply constraint 'le' to supplied value {value!r}"
            )

    def _validate_min_length(self, value: typing.Any):
        try:
            if not (len(value) >= self.min_length):
                raise ValidationError(
                    "too_short",
                    {
                        "field_type": "Value",
                        "min_length": self.min_length,
                        "actual_length": len(value),
                    },
                )
        except TypeError:
            raise TypeError(
                f"Unable to apply constraint 'min_length' to supplied value {value!r}"
            )

    def _validate_max_length(self, value: typing.Any):
        try:
            actual_length = len(value)
            if actual_length > self.max_length:
                raise ValidationError(
                    f"Value is too long. {actual_length} > {self.max_length}",
                    {
                        "field_type": "Value",
                        "max_length": self.max_length,
                        "actual_length": actual_length,
                    },
                )
        except TypeError:
            raise TypeError(
                f"Unable to apply constraint 'max_length' to supplied value {value!r}"
            )

    def _validate_pattern(self, value: typing.Any):
        try:
            if not re.match(self.pattern, value):
                raise ValidationError(
                    f"Field value '{value}' does not match pattern",
                    params={"pattern": self.pattern, "value": value},
                )
        except TypeError:
            raise TypeError(
                f"Unable to apply constraint 'pattern' to supplied value {value!r}"
            )


def is_mini_annotated(typ) -> bool:
    origin = get_origin(typ)
    return (
        origin
        and origin is Annotated
        and hasattr(typ, "__metadata__")
        and Attrib in [inst.__class__ for inst in typ.__metadata__]
    )


def is_type(typ):
    try:
        is_typ = isinstance(typ, type)
    except TypeError:
        is_typ = False
    return is_typ


def is_initvar_type(typ):
    if hasattr(typ, "type"):
        if isinstance(typ, InitVar):
            return typ.__class__.__name__ == "InitVar"
        return hasattr(typ, "__name__") and typ.__name__ == "InitVar"
    return False


def is_class_var_type(typ) -> bool:
    return typ is typing.ClassVar or get_origin(typ) is typing.ClassVar


def get_type(typ):
    if is_type(typ):
        return typ

    if is_optional_type(typ):
        type_args = get_args(typ)
        if type_args:
            return get_type(type_args[0])
        else:
            return

    origin = get_origin(typ)
    if is_type(origin):
        return origin

    type_args = get_args(typ)
    if len(type_args) > 0:
        return get_type(type_args[0])


def is_optional_type(typ):
    if hasattr(typ, "__origin__") and typ.__origin__ is typing.Union:
        return NoneType in typ.__args__
    elif typ is typing.Optional:
        return True
    return False


def is_collection(typ) -> typing.Tuple[bool, typing.Optional[type]]:
    origin = get_origin(typ)
    if origin and origin in (
        list,
        tuple,
        frozenset,
        set,
        collections.deque,
    ):
        return True, origin
    return False, None


def is_builtin_type(typ):
    typ = typ if isinstance(typ, type) else type(typ)
    return typ.__module__ in ("builtins", "__builtins__")


class MiniAnnotated:
    __slots__ = ()

    def __init_subclass__(cls, **kwargs):
        raise TypeError(f"Cannot subclass {cls.__module__}.MiniAnnotated")

    def __new__(cls, *args, **kwargs):
        raise TypeError("Type MiniAnnotated cannot be instantiated.")

    @typing._tp_cache
    def __class_getitem__(cls, params):
        if not isinstance(params, tuple):
            params = (params, Attrib())

        if len(params) != 2:
            raise TypeError(
                "MiniAnnotated[...] should be used with exactly two arguments (a type and an Attrib)."
            )

        typ = params[0]

        actual_typ = get_type(typ)
        if actual_typ is None:
            raise ValueError("'{}' is not a type".format(params[0]))

        query = params[1]
        if not isinstance(query, Attrib):
            raise TypeError("Parameter '{}' must be instance of Attrib".format(1))
        return Annotated[typ, query]
