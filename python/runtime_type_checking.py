from typing import Callable, get_type_hints


def typechecked_call[**P, T](c: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
    """
    This is a crude implementation of runtime type checking.

    After passing in a callable and it's args and kwards, each argument is
    checked against the type annotations of the callable (if they are present)
    and if they do not match, raises a TypeError.

    Because kwargs are a dict and args are a list, they need to be checked in
    slightly different ways.

    The functions type annotations themseles are quite complicated, the
    `[**P, T]` are inline typevar and paramspec definitions respectively. The
    callable is annotated with the Callable type, with the paramerterised values
    of the `P` (the paramspec) and the `T` (the return type). The args and
    kwargs are annotated with paramspec args and kwargs respectively. The return
    type for the function is the `T` typevar defined previously.
    """

    exception_string = "Argument '{}' of type {} does not match type annotation for argument '{}' of type {}"

    types = get_type_hints(c)

    for a, t in zip(args, types):
        if type(a) is not types[t]:
            raise TypeError(exception_string.format(a, type(a), t, types[t]))

    for key, value in kwargs.items():
        if key in types.keys():
            if type(value) is not types[key]:
                raise TypeError(
                    exception_string.format(value, type(value), key, types[key])
                )

    return c(*args, **kwargs)


def add(a: int, b: int) -> int:
    """Basic function using args"""
    return a + b


def hello(name: str, age: int) -> str:
    """Basic function using kwargs"""
    return f"Name: {name}, age: {age}"


# Both of these will work just fine
typechecked_call(add, 1, 2)
typechecked_call(hello, name="Matt", age=30)

# This will fail
try:
    typechecked_call(add, 1, "2")
except TypeError as e:
    print(e)

# As will this
try:
    typechecked_call(hello, name="Matt", age=False)
except TypeError as e:
    print(e)
