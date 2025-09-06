from dataclasses import dataclass

from tabulate import tabulate


@dataclass
class Person:
    name: str
    age: int


people = [Person("Bob", 25), Person("Steve", 30), Person("Dave", 35)]

print(tabulate(people, headers="keys"))
