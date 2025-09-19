import sys
from traceback import extract_tb
from types import TracebackType
from typing import Type

from tabulate import tabulate

"""
By overwriting the default execepthook, we can use our own custom exception handler.

The function is passed the exception type, the exception instance and a
traceback object.

By extracting the stack summary from the traceback, we can select the first
stack and grab info about the exception, such as filename and line number. We
can then process this however we see fit. Here we are just printing it to
stdout, but we could process this into a log entry or have custom behavour
depending on the exception type.
"""


def custom_excepthook(
    type: Type[BaseException], value: BaseException, traceback: TracebackType | None, /
) -> None:
    if traceback:
        tb_ss = extract_tb(traceback)[0]
        filename, lineno = tb_ss.filename, tb_ss.lineno

    tab = tabulate(
        [
            ("Exception Type", type.__name__),
            ("Exception Value", value),
            ("Exception Origin", f"{filename}, line {lineno}" if traceback else None),
        ],
        tablefmt="grid",
    )
    print(tab)


sys.excepthook = custom_excepthook

raise ValueError("This is a value error")
