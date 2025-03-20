import json
import os
from typing import Any, TypeVar

from google.protobuf.json_format import ParseDict
from google.protobuf.message import Message
from ruamel.yaml import YAML, YAMLError

T = TypeVar("T", bound=Message)


def read_yaml_file(
    instance: T,
    file: str,
    strict: bool = False,
) -> T:
    if not isinstance(instance, Message):
        raise TypeError(f"{type(instance).__name__} must be a protobuf message instance")

    yaml = YAML()
    with open(file, encoding="utf-8") as f:
        try:
            yaml_data = yaml.load(f)
        except YAMLError as e:
            raise ValueError("Invalid YAML file") from e

    if not isinstance(yaml_data, dict):
        raise ValueError("data must be a dictionary")

    if not _validate_dict_keys(yaml_data):
        raise ValueError("all dictionary keys must be strings recursively")

    ParseDict(yaml_data, instance, ignore_unknown_fields=not strict)
    return instance


def read_yaml_string(
    instance: T,
    data: str,
    strict: bool = False,
) -> T:
    if not isinstance(instance, Message):
        raise TypeError(f"{type(instance).__name__} must be a protobuf message instance")

    yaml = YAML()
    try:
        yaml_data = yaml.load(data)
    except YAMLError as e:
        raise ValueError("Invalid YAML string") from e

    if not isinstance(yaml_data, dict):
        raise ValueError("data must be a dictionary")

    if not _validate_dict_keys(yaml_data):
        raise ValueError("all dictionary keys must be strings recursively")

    ParseDict(yaml_data, instance, ignore_unknown_fields=not strict)
    return instance


def read_json_file(
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


def read_json_string(
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


def read_dict(
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


def read_environ(
    instance: T,
    mapping: dict[str, tuple[str, str, Any]],
    strict: bool = False,
) -> T:
    if not isinstance(instance, Message):
        raise TypeError(f"{type(instance).__name__} must be a protobuf message instance")

    for env_var, (path, value_type, default) in mapping.items():
        raw_value = os.getenv(env_var, None)

        if raw_value is None and default is None:
            continue

        parsed_value: Any

        if value_type == "str":
            if raw_value is not None:
                parsed_value = raw_value
            elif isinstance(default, str):
                parsed_value = default
            else:
                raise TypeError(f"default value for '{env_var}' should be str, got {type(default)}")

        elif value_type == "int":
            if raw_value is not None:
                parsed_value = int(raw_value)
            elif isinstance(default, int):
                parsed_value = default
            else:
                raise TypeError(f"default value for '{env_var}' should be int, got {type(default)}")

        elif value_type == "float":
            if raw_value is not None:
                parsed_value = float(raw_value)
            elif isinstance(default, float):
                parsed_value = default
            else:
                raise TypeError(f"default value for '{env_var}' should be float, got {type(default)}")

        elif value_type == "bool":
            if raw_value is not None:
                parsed_value = raw_value.lower() in ("true", "yes", "on", "1")
            elif isinstance(default, bool):
                parsed_value = default
            else:
                raise TypeError(f"default value for '{env_var}' should be bool, got {type(default)}")

        elif value_type == "list[str]":
            if raw_value is not None:
                parsed_value = [v.strip() for v in raw_value.split(",") if v.strip()]
            elif isinstance(default, str):
                parsed_value = [v.strip() for v in default.split(",") if v.strip()]
            elif isinstance(default, list):
                if all(isinstance(v, str) for v in default):
                    parsed_value = default
                else:
                    raise TypeError(f"default value for '{env_var}' should be list[str], got list with mixed types")
            else:
                raise TypeError(f"default value for '{env_var}' should be str or list[str], got {type(default)}")

        else:
            raise TypeError(f"unsupported value_type {value_type} for env_var {env_var}")

        _set_nested_attr(instance, path.split("."), parsed_value, strict)

    return instance


def _set_nested_attr(
    message: Message,
    path: list[str],
    value: Any,
    strict: bool,
):
    for field in path[:-1]:
        if not message.HasField(field) and strict:
            raise AttributeError(f"field '{field}' not found in {message.DESCRIPTOR.full_name}")
        message = getattr(message, field)

    last_field = path[-1]

    if not hasattr(message, last_field):
        if strict:
            raise AttributeError(f"field '{last_field}' not found in {message.DESCRIPTOR.full_name}")
        return

    field_descriptor = message.DESCRIPTOR.fields_by_name[last_field]

    if field_descriptor.label == field_descriptor.LABEL_REPEATED:
        if isinstance(value, list):
            field_list = getattr(message, last_field)
            field_list[:] = []
            field_list.extend(value)
        else:
            raise TypeError(f"expected a list for repeated field '{last_field}', got {type(value)}")
        return

    setattr(message, last_field, value)
