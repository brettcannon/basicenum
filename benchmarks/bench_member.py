import enum
import pickle

import basicenum


class StdlibEnum(enum.Enum):
    member = 42


class BasicEnum(basicenum.Enum):
    member: int = 42


def bench_access(enum):
    for _ in range(500_000):
        x = enum.member


def stdlib_access():
    bench_access(StdlibEnum)


def basicenum_access():
    bench_access(BasicEnum)


def bench_equality(enum):
    for _ in range(250_000):
        x = enum.A == enum.B


def stdlib_equality():
    class Enum(enum.Enum):
        A = "A"
        B = "B"

    bench_equality(Enum)


def basicenum_equality():
    class Enum(basicenum.Enum):
        A: str = "A"
        B: str = "B"

    bench_equality(Enum)


def bench_repr(member):
    for _ in range(100_000):
        x = repr(member)


def stdlib_repr():
    bench_repr(StdlibEnum.member)


def basicenum_repr():
    bench_repr(BasicEnum.member)


def bench_hash(member):
    for _ in range(200_000):
        x = hash(member)


def stdlib_hash():
    bench_hash(StdlibEnum.member)


def basicenum_hash():
    bench_hash(BasicEnum.member)


def bench_pickling(member):
    for _ in range(25_000):
        pickle.dumps(member)


def stdlib_pickling():
    bench_pickling(StdlibEnum.member)


def basicenum_picking():
    bench_pickling(BasicEnum.member)


def bench_unpickling(member):
    pickle_ = pickle.dumps(member)
    for _ in range(25_000):
        pickle.loads(pickle_)


def stdlib_unpickling():
    bench_unpickling(StdlibEnum.member)


def basicenum_unpickling():
    bench_unpickling(BasicEnum.member)


__benchmarks__ = [
    (stdlib_access, basicenum_access, "member access"),
    (stdlib_equality, basicenum_equality, "member equality"),
    (stdlib_repr, basicenum_repr, "member repr"),
    (stdlib_hash, basicenum_hash, "member hash"),
    (stdlib_pickling, basicenum_picking, "pickling"),
    (stdlib_unpickling, basicenum_unpickling, "unpickling"),
]
