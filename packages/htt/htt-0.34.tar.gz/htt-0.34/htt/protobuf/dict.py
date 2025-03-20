from typing import Any, TypeVar

from google.protobuf.json_format import MessageToDict, ParseDict
from google.protobuf.message import Message

T = TypeVar("T", bound=Message)


def from_dict(
    instance: T,
    data: dict[str, Any],
    strict: bool = False,
) -> T:
    if not isinstance(instance, Message):
        raise TypeError(f"{type(instance).__name__} must be a protobuf message instance")

    if not isinstance(data, dict):
        raise ValueError("data must be a dictionary")

    if not _validate_dict_keys(data):
        raise ValueError("all dictionary keys must be strings recursively")

    ParseDict(data, instance, ignore_unknown_fields=not strict)
    return instance


def _validate_dict_keys(
    obj: Any,
) -> bool:
    if isinstance(obj, dict):
        return all(isinstance(k, str) and _validate_dict_keys(v) for k, v in obj.items())
    elif isinstance(obj, list):
        return all(_validate_dict_keys(item) for item in obj)
    return True


def to_dict(
    instance: Message,
) -> dict:
    if not isinstance(instance, Message):
        raise TypeError(f"{type(instance).__name__} must be a protobuf message instance")

    return MessageToDict(
        instance,
        preserving_proto_field_name=True,
        always_print_fields_with_no_presence=True,
    )
