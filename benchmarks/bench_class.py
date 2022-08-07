import enum

import basicenum

AUTO_BENCH = 1_000
STR_BENCH = 1_000
CONST_BENCH = 1_000
CUSTOM_BENCH = 1_000
UNIQUE_BENCH = 1_000


def stdlib_auto():
    for _ in range(AUTO_BENCH):

        class Enum(enum.Enum):
            v1 = enum.auto()
            v2 = enum.auto()
            v3 = enum.auto()
            v4 = enum.auto()
            v5 = enum.auto()


def basicenum_auto():
    for _ in range(AUTO_BENCH):

        class Enum(basicenum.Enum):
            v1: int
            v2: int
            v3: int
            v4: int
            v5: int


def stdlib_str():
    for _ in range(STR_BENCH):

        class Enum(enum.Enum):
            RED = "RED"
            GREEN = "GREEN"
            BLUE = "BLUE"


def basicenum_str():
    for _ in range(STR_BENCH):

        class Enum(basicenum.Enum):
            RED: str
            GREEN: str
            BLUE: str


def stdlib_constants():
    for _ in range(CONST_BENCH):

        class Enum(enum.Enum):
            RED = "red"
            GREEN = "green"
            BLUE = "blue"


def basicenum_constants():
    for _ in range(CONST_BENCH):

        class Enum(basicenum.Enum):
            RED: str = "red"
            GREEN: str = "green"
            BLUE: str = "blue"


def stdlib_custom_values():
    class LowerEnum(enum.Enum):
        def _generate_next_value_(name, start, count, last_values):
            return name.lower()

    for _ in range(CUSTOM_BENCH):

        class Enum(LowerEnum):

            RED = enum.auto()
            GREEN = enum.auto()
            BLUE = enum.auto()


def basicenum_custom_values():
    def lowercase(cls, name, index):
        return name.lower()

    for _ in range(CUSTOM_BENCH):

        class Enum(basicenum.Enum, value=lowercase):
            RED: str
            GREEN: str
            BLUE: str


def stdlib_unique():
    for _ in range(UNIQUE_BENCH):

        @enum.unique
        class Enum(enum.Enum):
            v1 = enum.auto()
            v2 = enum.auto()
            v3 = enum.auto()
            v4 = enum.auto()
            v5 = enum.auto()


def basicenum_unique():
    for _ in range(UNIQUE_BENCH):

        class Enum(basicenum.Enum, unique=True):
            v1: int
            v2: int
            v3: int
            v4: int
            v5: int


def bench_functional(func):
    for _ in range(1_000):
        func("Animal", ["ANT", "BEE", "CAT", "DOG"])


def stdlib_functional():
    bench_functional(enum.Enum)


def basicenum_functional():
    bench_functional(basicenum.create)


def compat_functional():
    bench_functional(basicenum.compat_create)


__benchmarks__ = [
    (stdlib_auto, basicenum_auto, "class w/ int"),
    (stdlib_str, basicenum_str, "class w/ str"),
    (stdlib_constants, basicenum_constants, "class w/ constants"),
    (stdlib_custom_values, basicenum_custom_values, "class w/ value func"),
    (stdlib_unique, basicenum_unique, "class w/ uniqueness"),
    (stdlib_functional, basicenum_functional, "functional API"),
    (stdlib_functional, compat_functional, "compat functional API"),
]
