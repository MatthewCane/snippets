from dataclasses import dataclass
from typing import Any


class Registry:
    """
    An example of the registry pattern as a Python class.

    Any keyword arguments passed to the constructor are added
    to an instance variable _registry which is a dict of the
    keys and values.

    Extra checks are done when setting to ensure values are not
    overwritten and all keys are stored and retrieved as
    lowercase.
    """

    def __init__(self, **items: Any):
        self._registry = {}
        self.put(**items)

    def get(self, key: str) -> Any:
        return self._registry.get(key.lower())

    def put(self, **items: Any):
        for name, obj in items.items():
            if self._registry.get(name, None) is not None:
                raise ValueError(f"The key {name} already exists in the registy")

            self._registry[name.lower()] = obj

    def __str__(self):
        return str(self._registry)

    def __repr__(self):
        return self.__str__()


@dataclass
class Stage:
    account: int
    region: str


stages = Registry(
    prod=Stage(1234, "eu"), staging=Stage(5678, "us"), dev=Stage(1357, "cn")
)

print(f"{stages = }")

print(f"{stages.get("staging") = }")

print(f"{stages.get("prod").account = }")
