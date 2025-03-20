import os
from dataclasses import is_dataclass
from types import SimpleNamespace
from typing import Any, TypeVar, cast

import dacite
from ruamel.yaml import YAML

T = TypeVar("T", bound=SimpleNamespace)


def read_yaml_file(
    cls: type[T],
    file: str,
    strict: bool = False,
) -> T:
    if not is_dataclass(cls):
        raise TypeError(f"{cls.__name__} must be a dataclass type")

    with open(file) as f:
        yaml = YAML()
        data = yaml.load(f)

    if not isinstance(data, dict):
        raise ValueError("data must be a dictionary")

    if not all(isinstance(k, str) for k in data.keys()):
        raise ValueError("all keys in the dictionary must be strings")

    instance = dacite.from_dict(
        data_class=cls,
        data=data,
        config=dacite.Config(strict=strict),
    )

    return instance


def read_dict(
    cls: type[T],
    data: dict[str, Any],
    strict: bool = False,
) -> T:
    if not is_dataclass(cls):
        raise TypeError(f"{cls.__name__} must be a dataclass type")

    if not isinstance(data, dict):
        raise ValueError("data must be a dictionary")

    if not all(isinstance(k, str) for k in data.keys()):
        raise ValueError("all keys in the dictionary must be strings")

    instance = dacite.from_dict(
        data_class=cls,
        data=data,
        config=dacite.Config(strict=strict),
    )

    return cast(T, instance)


def read_environ(
    cls: type[T],
    mapping: dict[str, tuple[str, str, Any]],
    strict: bool = False,
) -> T:
    if not is_dataclass(cls):
        raise TypeError(f"{cls.__name__} must be a dataclass type")

    instance: T = cls()
    for env_var, (path, value_type, default) in mapping.items():
        raw_value = os.getenv(env_var, None)

        if raw_value is None:
            parsed_value = default
        elif value_type == "int":
            parsed_value = int(raw_value)
        elif value_type == "float":
            parsed_value = float(raw_value)
        elif value_type == "bool":
            parsed_value = raw_value.lower() in ("true", "1", "yes", "on")
        else:
            parsed_value = raw_value

        _set_nested_attr(instance, path.split("."), parsed_value, strict)

    return instance


def _set_nested_attr(
    object: Any,
    keys: list[str],
    value: Any,
    strict: bool,
):
    if len(keys) == 1:
        setattr(object, keys[0], value)
    else:
        next_object = getattr(object, keys[0], None)
        if next_object is None or not is_dataclass(next_object):
            if strict:
                raise AttributeError(f"set attr failed at {'.'.join(keys)}")
        _set_nested_attr(next_object, keys[1:], value, strict)
