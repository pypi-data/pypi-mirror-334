import json
from typing import TypeVar

from google.protobuf.json_format import MessageToJson, ParseDict
from google.protobuf.message import Message

T = TypeVar("T", bound=Message)


def from_json_file(
    instance: T,
    file: str,
    strict: bool = False,
) -> T:
    if not isinstance(instance, Message):
        raise TypeError(f"{type(instance).__name__} must be a protobuf message instance")

    with open(file, encoding="utf-8") as f:
        try:
            json_data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError("Invalid JSON file") from e

    if not isinstance(json_data, dict):
        raise ValueError("data must be a dictionary")

    ParseDict(json_data, instance, ignore_unknown_fields=not strict)
    return instance


def from_json_string(
    instance: T,
    data: str,
    strict: bool = False,
) -> T:
    if not isinstance(instance, Message):
        raise TypeError(f"{type(instance).__name__} must be a protobuf message instance")

    try:
        json_data = json.loads(data)
    except json.JSONDecodeError as e:
        raise ValueError("Invalid JSON string") from e

    if not isinstance(json_data, dict):
        raise ValueError("data must be a dictionary")

    ParseDict(json_data, instance, ignore_unknown_fields=not strict)
    return instance


def to_json_file(
    instance: Message,
    file: str,
    indent: int | None = 2,
) -> None:
    if not isinstance(instance, Message):
        raise TypeError(f"{type(instance).__name__} must be a protobuf message instance")

    data = MessageToJson(
        instance,
        indent=indent,
        always_print_fields_with_no_presence=True,
    )

    with open(file, "w", encoding="utf-8") as f:
        f.write(data)


def to_json_string(
    instance: Message,
    indent: int | None = 2,
) -> str:
    if not isinstance(instance, Message):
        raise TypeError(f"{type(instance).__name__} must be a protobuf message instance")

    return MessageToJson(
        instance,
        indent=indent,
        always_print_fields_with_no_presence=True,
    )
