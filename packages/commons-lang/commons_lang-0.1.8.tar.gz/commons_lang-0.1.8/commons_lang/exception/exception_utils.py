from typing import Type


def raise_exception(exception_type: Type[Exception], exception_message):
    raise exception_type(exception_message)
