import os
from typing import Any

"""
Parse environment variables.
"""


def parse_env_vars(
    required: list[str] | None = None, optional: dict[str, str | None] | None = None
) -> dict[str, Any]:
    """Parse environment variables into a dictionary.

    Given a list of args and kwargs, use them as keys to parse the environment
    variables and return a dictionary with the values. args are required, kwargs
    are optional and use the value as default.
    """
    required = required or []
    optional = optional or {}

    if missing_vars := set(required).difference(os.environ):
        raise ValueError(
            f"Missing required environment variables: {', '.join(sorted(missing_vars))}"
        )

    required_vars = {key: os.environ[key] for key in required}
    optional_vars = {
        key: os.environ.get(key, default) for key, default in optional.items()
    }

    return {**optional_vars, **required_vars}


os.environ["foo"] = "bar"

assert parse_env_vars(required=["foo"]) == {"foo": "bar"}

assert parse_env_vars(optional={"var": None}) == {"var": None}

assert parse_env_vars(required=["foo"], optional={"baz": "default"}) == {
    "foo": "bar",
    "baz": "default",
}

assert parse_env_vars(required=["boo", "zoo"])
