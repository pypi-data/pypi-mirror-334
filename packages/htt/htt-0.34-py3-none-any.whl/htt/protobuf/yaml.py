from io import StringIO
from typing import TypeVar

from google.protobuf.json_format import MessageToDict, ParseDict
from google.protobuf.message import Message
from ruamel.yaml import YAML, YAMLError
from ruamel.yaml.scalarstring import DoubleQuotedScalarString

from htt.protobuf.dict import _validate_dict_keys

T = TypeVar("T", bound=Message)


def from_yaml_file(
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


def from_yaml_string(
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


def to_yaml_file(
    instance: Message,
    file: str,
    indent: int | None = 2,
) -> None:
    if not isinstance(instance, Message):
        raise TypeError(f"{type(instance).__name__} must be a protobuf message instance")

    yaml = YAML()
    yaml.allow_unicode = True
    yaml.width = 1048576

    if indent is None:
        yaml.default_flow_style = True
    else:
        yaml.default_flow_style = False
        yaml.indent(mapping=indent, sequence=indent, offset=indent)

    data = MessageToDict(
        instance,
        preserving_proto_field_name=True,
        always_print_fields_with_no_presence=True,
    )

    quoted_data = _quote_yaml_strings(data)

    with open(file, "w", encoding="utf-8") as f:
        yaml.dump(quoted_data, f)


def to_yaml_string(
    instance: Message,
    indent: int | None = 2,
) -> str:
    if not isinstance(instance, Message):
        raise TypeError(f"{type(instance).__name__} must be a protobuf message instance")

    yaml = YAML()
    yaml.allow_unicode = True
    yaml.width = 1048576

    if indent is None:
        yaml.default_flow_style = True
    else:
        yaml.default_flow_style = False
        yaml.indent(mapping=indent, sequence=indent, offset=indent)

    data = MessageToDict(
        instance,
        preserving_proto_field_name=True,
        always_print_fields_with_no_presence=True,
    )

    quoted_data = _quote_yaml_strings(data)

    stream = StringIO()
    yaml.dump(quoted_data, stream)
    return stream.getvalue()


def _quote_yaml_strings(data):
    if isinstance(data, dict):
        return {k: _quote_yaml_strings(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [_quote_yaml_strings(v) for v in data]
    elif isinstance(data, str):
        return DoubleQuotedScalarString(data)
    return data
