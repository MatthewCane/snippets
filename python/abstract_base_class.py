import base64
import json
import pickle
from abc import ABC, abstractmethod


class AbstractStorage(ABC):
    def __init__(self, path):
        self.path = path
        self.type = None

    @abstractmethod
    def store(self, data): ...

    @abstractmethod
    def load(self): ...

    def verify(self, data):
        return data == self.load()


class JsonStore(AbstractStorage):
    def store(self, data):
        self.type = type(data)
        with open(self.path, "w") as f:
            json.dump(data, f)

    def load(self):
        with open(self.path, "r") as f:
            return json.load(f)


class PickleStore(AbstractStorage):
    def store(self, data):
        self.type = type(data)
        with open(self.path, "wb") as f:
            pickle.dump(data, f)

    def load(self):
        with open(self.path, "rb") as f:
            return pickle.load(f)


class Base64Store(AbstractStorage):
    def store(self, data):
        self.type = type(data)
        with open(self.path, "wb") as f:
            f.write(base64.b64encode(str(data).encode("utf-8")))

    def load(self):
        with open(self.path, "rb") as f:
            return base64.b64decode(f.read()).decode("utf-8")


data = {
    "name": "Matthew",
    "age": 30,
    "city": "New York",
    "country": "USA",
    "email": "matthew@example.com",
    "phone": "555-1234",
    "address": "123 Main St",
    "zip": "10001",
    "state": "NY",
}

jstore = JsonStore("data.json")
jstore.store(data)
jstore.verify(data)
print(jstore.load())
print(type(jstore.load()))

pstore = PickleStore("data.pickle")
pstore.store(data)
pstore.verify(data)
print(pstore.load())
print(type(pstore.load()))

bstore = Base64Store("data.b64")
bstore.store(data)
bstore.verify(data)
print(bstore.load())
print(type(bstore.load()))
