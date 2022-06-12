from functools import update_wrapper


def countcalls(func):
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)

    wrapper.calls = 0
    # return wrapper
    return update_wrapper(wrapper, func)


def dummy(func):
    def dummy_wrapper(*args, **kwargs):
        print("dummy")
        return func(*args, **kwargs)

    # return dummy_wrapper
    return update_wrapper(dummy_wrapper, func)


@countcalls
@dummy
def foo():
    """Документация"""
    pass


@countcalls
@dummy
def bar():
    pass


def main():
    foo()
    # bar()
    print("foo was called", foo.calls, "times")
    print(foo.__name__)
    print(foo.__doc__)


if __name__ == "__main__":
    main()
