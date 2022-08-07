import enum
import functools
import importlib
import pickle

from basicenum import compat


def bench(func, stdlib=enum, compat=compat):
    return functools.partial(func, stdlib), functools.partial(func, compat)


class StdlibEnum(enum.Enum):
    member = 42


class CompatEnum(enum.Enum):
    member = 42


def import_(module):
    for _ in range(100):
        importlib.reload(module)


def auto(module):
    for _ in range(1_000):

        class Enum(module.Enum):
            v1 = module.auto()
            v2 = module.auto()
            v3 = module.auto()
            v4 = module.auto()
            v5 = module.auto()


def generate(module):
    class AutoEnum(module.Enum):
        def _generate_next_value_(name, start, count, last_values):
            return name

    for _ in range(1_000):

        class Enum(AutoEnum):
            RED = module.auto()
            GREEN = module.auto()
            BLUE = module.auto()


def constants(module):
    for _ in range(1_000):

        class Enum(module.Enum):
            RED = "RED"
            GREEN = "GREEN"
            BLUE = "BLUE"


def functional(func):
    for _ in range(1_000):
        func("Animal", ["ANT", "BEE", "CAT", "DOG"])


# `enum.Enum` does such deep introspection it doesn't like being used with bench().
def stdlib_functional():
    functional(enum.Enum)


def compat_functional():
    functional(compat.create)


def isinstance_(module):
    class Enum(module.Enum):
        member = 42

    for _ in range(200_000):
        isinstance(Enum.member, Enum)


def iter_(module):
    class Enum(module.Enum):
        v1 = module.auto()
        v2 = module.auto()
        v3 = module.auto()
        v4 = module.auto()
        v5 = module.auto()

    for _ in range(100_000):
        list(Enum)


def call(module):
    class Enum(module.Enum):
        member = 42

    for _ in range(100_000):
        Enum(42)


def getitem(module):
    class Enum(module.Enum):
        member = 42

    for _ in range(100_000):
        Enum["member"]


def contains(module):
    class Enum(module.Enum):
        member = 42

    for _ in range(100_000):
        x = Enum.member in Enum


def access(module):
    class Enum(module.Enum):
        member = 42

    for _ in range(500_000):
        x = Enum.member


def value(module):
    class Enum(module.Enum):
        member = 42

    member = Enum.member

    for _ in range(500_000):
        member.value


def equality(module):
    class Enum(module.Enum):
        A = "A"
        B = "B"

    for _ in range(250_000):
        x = Enum.A == Enum.B


def repr_(module):
    class BenchEnum(module.Enum):
        member = 42

    for _ in range(100_000):
        x = repr(BenchEnum.member)


def hash_(module):
    class Enum(module.Enum):
        member = 42

    for _ in range(200_000):
        x = hash(Enum.member)


def pickling(enum_):

    for _ in range(25_000):
        pickle.dumps(enum_.member)


def unpickling(enum_):
    pickle_ = pickle.dumps(enum_.member)
    for _ in range(25_000):
        pickle.loads(pickle_)


def members(module):
    class Enum(module.Enum):
        RED = "RED"

    for _ in range(200_000):
        Enum.__members__


def unique(module):
    for _ in range(1_000):

        @module.unique
        class Enum(module.Enum):
            MERCURY = "MERCURY"
            VENUS = "VENUS"
            EARTH = "EARTH"
            MARS = "MARS"
            JUPITER = "JUPITER"
            SATURN = "SATURN"
            URANUS = "URANUS"
            NEPTUNE = "NEPTUME"


__benchmarks__ = [
    (*bench(import_), "import"),
    (*bench(auto), "creation w/ `auto()`"),
    (*bench(generate), "`_generate_next_value_()`"),
    (*bench(constants), "creation w/ constants"),
    (stdlib_functional, compat_functional, "functional API"),
    (*bench(isinstance_), "isinstance(..., Enum)"),
    (*bench(iter_), "`iter(Enum)`"),
    (*bench(call), "`Enum(...)`"),
    (*bench(getitem), "`Enum[...]`"),
    (*bench(contains), "`... in Enum`"),
    (*bench(access), "member access"),
    (*bench(value), "value access"),
    (*bench(equality), "equality"),
    (*bench(repr_), "repr"),
    (*bench(hash_), "hashing"),
    (*bench(pickling, StdlibEnum, CompatEnum), "pickling"),
    (*bench(unpickling, StdlibEnum, CompatEnum), "unpickling"),
    (*bench(members), "`__members__`"),
    (*bench(unique), "`@unique`"),
]
