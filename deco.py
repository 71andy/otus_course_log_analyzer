#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import update_wrapper


def disable():
    """
    Disable a decorator by re-assigning the decorator's name
    to this function. For example, to turn off memoization:

    >>> memo = disable

    """
    return


def decorator():
    """
    Decorate a decorator so that it inherits the docstrings
    and stuff from the function it's decorating.
    """
    return


def countcalls(func):
    """Decorator that counts calls made to the function decorated."""

    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)

    wrapper.calls = 0
    return update_wrapper(wrapper, func)


def memo(func):
    """
    Memoize a function so that it caches all return values for
    faster future lookups.
    """
    cache = {}

    def wrapper(*args, **kwargs):
        if len(kwargs) > 0:
            return func(*args, **kwargs)
        if args in cache:
            print(f"cached value was found: {func.__name__}{args} == {cache[args]}")
            return cache[args]

        cache[args] = func(*args)
        return cache[args]

    return update_wrapper(wrapper, func)


def n_ary(func):
    """
    Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x.
    """

    def wrapper(*args, **kwargs):

        if len(args) == 1:
            return args[0]
        else:
            result = func(args[0], args[1], **kwargs)
            for i in range(2, len(args)):
                result = func(result, args[i], **kwargs)
            return result

    return update_wrapper(wrapper, func)


def trace(s):
    """Trace calls made to function decorated.

    @trace("____")
    def fib(n):
        ....

    >>> fib(3)
     --> fib(3)
    ____ --> fib(2)
    ________ --> fib(1)
    ________ <-- fib(1) == 1
    ________ --> fib(0)
    ________ <-- fib(0) == 1
    ____ <-- fib(2) == 2
    ____ --> fib(1)
    ____ <-- fib(1) == 1
     <-- fib(3) == 3

    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f"{s * wrapper.depth} --> {func.__name__}({args[0]})")
            wrapper.depth += 1
            result = func(*args, **kwargs)
            wrapper.depth -= 1
            print(f"{s * wrapper.depth} <-- {func.__name__}({args[0]}) == {result}")
            return result

        wrapper.depth = 0

        return update_wrapper(wrapper, func)

    return decorator


@countcalls
@memo
@n_ary
def foo(a, b):
    return a + b


@countcalls
@n_ary
@memo
def bar(a, b):
    return a * b


@countcalls
@trace("____")
@memo
def fib(n):
    """Some doc"""
    return 1 if n <= 1 else fib(n - 1) + fib(n - 2)


def main():
    print(foo(4, 3))
    print(foo(4, 3, 2))
    print(foo(4, 3))
    print("foo was called", foo.calls, "times")

    print(bar(4, 3))
    print(bar(4, 3, 2))
    print(bar(4, 3, 2, 1))
    print("bar was called", bar.calls, "times")

    print(fib.__doc__)
    fib(5)
    print(fib.calls, "calls made")
    fib(6)
    print(fib.calls, "calls made")


if __name__ == "__main__":
    main()
