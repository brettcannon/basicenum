import importlib


def bench_import(module):
    for _ in range(100):
        importlib.reload(module)


def stdlib():
    """Reload `enum`"""
    import enum

    bench_import(enum)


def basicenum():
    """Reload basicenum"""
    import basicenum

    bench_import(basicenum)


__benchmarks__ = [(stdlib, basicenum, "import")]
