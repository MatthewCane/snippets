import os
from dataclasses import _MISSING_TYPE, dataclass, fields, is_dataclass
from typing import Any, ClassVar, Dict, Protocol, Type


class DataclassLike(Protocol):
    """A protocol representing a dataclass-like structure."""

    __dataclass_fields__: ClassVar[Dict[str, Any]]


def parse_env_vars[T: DataclassLike](options: Type[T]) -> T:
    """Parse environment variables using a dataclass.

    Given a dataclass, use the field names as keys to parse the environment
    variables and return an instance of the dataclass with the values. Fields
    without a default value are required, fields with a default value are optional
    and use the default if the environment variable is not set.

    Bool fields are treated specially, if the envvar is set to any of "0", "false"
    or "False" then the value is False, otherwise it is True if the envvar is set.
    """

    def cast_type(value: str, to_type: Type) -> Any:
        false_values = ("0", "false", "False")

        if isinstance(to_type, bool):
            return False if value in false_values else True
        return to_type(value)

    if not is_dataclass(options):
        raise ValueError("options argument must be a dataclass")

    # Extract the required and optional envvars from the options class
    required = [
        {"key": f.name, "type": f.type}
        for f in fields(options)
        if isinstance(f.default, _MISSING_TYPE)
    ]
    optional = [
        {"key": f.name, "type": f.type, "default": f.default}
        for f in fields(options)
        if not isinstance(f.default, _MISSING_TYPE)
    ]

    # Check all required vars exist in environ
    if missing_vars := set([f["key"] for f in required]).difference(os.environ):
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )

    # Fetch the required vars values and cast the required values into
    # the types specified in the dataclass
    required_vars = {}
    for item in required:
        key, _type = item["key"], item["type"]
        value = os.environ[key]
        try:
            value = cast_type(value, _type)
        except Exception:
            raise TypeError(
                f"Unable to cast value '{value}' from key '{key}' to type {_type}"
            )
        required_vars[key] = value

    # Do the same for optional vars, but use the default if not set
    optional_vars = {}
    for item in optional:
        key, _type, default = item["key"], item["type"], item["default"]
        value = os.environ.get(key, default)
        try:
            value = cast_type(value, _type)
        except Exception:
            raise TypeError(
                f"Unable to cast value '{value}' from key '{key}' to type {_type}"
            )
        optional_vars[key] = value

    return options(**required_vars, **optional_vars)


@dataclass
class Config:
    first_name: str
    age: int
    enabled: bool = False


os.environ["first_name"] = "foo"
os.environ["age"] = "30"
os.environ["enabled"] = "0"

# assert parse_env_vars(Config) == Config(first_name="foo", age=30, enabled=False)

# os.environ["enabled"] = ""

# assert parse_env_vars(Config) == Config(first_name="foo", age=30, enabled=False)
false_values = ("0", "false", "False")
value = "0"
to_type = bool

print(value in false_values)

if isinstance(to_type, bool):
    print(False if value in false_values else True)
else:
    print(to_type(value))
