import enum
import pickle

import pytest
from basicenum import compat


@pytest.mark.parametrize("create", [enum.Enum, compat.create])
class TestCreate:
    def test_name(self, create):
        enum_ = create("a", [])
        assert enum_.__qualname__ == "a"
        assert enum_.__name__ == "a"

    def test_qualname(self, create):
        enum_ = create("a", [], qualname="c.b.a")
        assert enum_.__name__ == "a"
        assert enum_.__qualname__ == "c.b.a"

    def test_module(self, create):
        enum_ = create("a", [], module="c.b")
        assert enum_.__module__ == "c.b"
        assert enum_.__name__ == "a"
        if not issubclass(enum_, enum.Enum):
            assert enum_.__qualname__ == "c.b.a"

    def test_member_order(self, create):
        enum_ = create("test_member_order", ["v1", "v2", "v3"])
        for value in range(1, 4):
            assert getattr(enum_, f"v{value}").value == value

    @pytest.mark.parametrize("separator", [" ", ",", ", "])
    def test_str_names(self, create, separator):
        names = separator.join(["v1", "v2", "v3"])
        enum_ = create("enum_", names)
        assert enum_.v1.value == 1
        assert enum_.v2.value == 2
        assert enum_.v3.value == 3

    def test_pairs_names(self, create):
        names = [("v1", 2), ("v2", 4), ("v3", 6)]
        enum_ = create("enum_", names)
        assert enum_.v1.value == 2
        assert enum_.v2.value == 4
        assert enum_.v3.value == 6

    def test_mapping_names(self, create):
        names = {"v1": 3, "v2": 6, "v3": 9}
        enum_ = create("enum_", names)
        assert enum_.v1.value == 3
        assert enum_.v2.value == 6
        assert enum_.v3.value == 9

    def test_subclass(self, create):
        class Sub:
            pass

        enum_ = create("enum_", [], type=Sub)
        assert issubclass(enum_, Sub)

    def test_start(self, create):
        enum_ = create("enum_", ["v1", "v2", "v3"], start=9)
        assert enum_.v1.value == 9
        assert enum_.v2.value == 10
        assert enum_.v3.value == 11


@pytest.mark.parametrize("module", [enum, compat])
class TestClass:
    def test_auto(self, module):
        class Enum(module.Enum):
            v1 = module.auto()
            v2 = module.auto()
            v3 = module.auto()

        for attr in {"v1", "v2", "v3"}:
            member = getattr(Enum, attr)
            assert member.name == attr
            assert member.value == int(attr[-1])

    def test_auto_interleave_int(self, module):
        class Enum(module.Enum):
            v1 = module.auto()
            v2 = 5
            v3 = module.auto()

        assert Enum.v1.value == 1
        assert Enum.v2.value == 5
        assert Enum.v3.value == 6

    def test_auto_generate(self, module):
        next_values = []

        class AutoEnum(module.Enum):
            def _generate_next_value_(*args):
                next_values.append(args)
                return args[0]

        class Enum(AutoEnum):
            A = module.auto()
            B = "HI"
            C = module.auto()

        assert Enum.A.value == "A"
        assert Enum.B.value == "HI"
        assert Enum.C.value == "C"

        assert len(next_values) == 2
        assert next_values[0] == ("A", 1, 0, [])
        assert next_values[1] == ("C", 1, 2, ["A", "HI"])

    def test_constants(self, module):
        class Enum(module.Enum):
            RED = "RED"
            GREEN = "GREEN"
            BLUE = "BLUE"

        for attr in {"RED", "GREEN", "BLUE"}:
            member = getattr(Enum, attr)
            assert member.name == attr
            assert member.value == attr

    def test_mixed_types(self, module):
        class Enum(module.Enum):
            v1 = 1
            v2 = "2"

        assert Enum.v1.value == 1
        assert Enum.v2.value == "2"

    def test_members(self, module):
        class Enum(module.Enum):
            v1 = 1
            v2 = 2
            v3 = 3

        assert Enum.__members__ == {"v1": Enum.v1, "v2": Enum.v2, "v3": Enum.v3}

    def test_isinstance(self, module):
        class Enum(module.Enum):
            v1 = module.auto()
            RED = "RED"

        assert isinstance(Enum.v1, Enum)
        assert isinstance(Enum.RED, Enum)

    def test_iter(self, module):
        class Enum(module.Enum):
            v1 = 1
            v2 = 2
            v3 = 3

        assert list(Enum) == [Enum.v1, Enum.v2, Enum.v3]

    def test_call_success(self, module):
        class Enum1(module.Enum):
            member = 42

        class Enum2(module.Enum):
            member = 42

        assert Enum1(42) == Enum1.member
        # Implicitly tests that memoization isn't problematic.
        assert Enum2(42) == Enum2.member

    def test_call_fail(self, module):
        class Enum(module.Enum):
            names = ()

        with pytest.raises(ValueError):
            Enum(42)

    def test_getitem_success(self, module):
        class Enum(module.Enum):
            member = 42

        assert Enum["member"] == Enum.member

    def test_getitem_fail(self, module):
        class Enum(module.Enum):
            pass

        with pytest.raises(KeyError):
            Enum["member"]

    def test_contains(self, module):
        class Enum(module.Enum):
            member = 42

        assert Enum.member in Enum


class TestBasicEnumClass:
    def test_auto_interleave_str(self):
        """Test interleaving arbitrary values between auto() calls.

        Stdlib enum deprecated this support and is slated for removal in
        Python 3.13.
        """

        class Enum(compat.Enum):
            v1 = compat.auto()
            v2 = "5"
            v3 = compat.auto()

        assert Enum.v1.value == 1
        assert Enum.v2.value == "5"
        assert Enum.v3.value == 2


class StdlibEnum(enum.Enum):
    v1 = enum.auto()
    v2 = enum.auto()


class CompatEnum(compat.Enum):
    v1 = compat.auto()
    v2 = compat.auto()


@pytest.mark.parametrize("enum_", [StdlibEnum, CompatEnum])
class TestMember:
    def test_identity(self, enum_):
        assert enum_.v1 is enum_.v1

    def test_exact_eq(self, enum_):
        assert enum_.v1 == enum_.v1

    def test_not_eq(self, enum_):
        assert enum_.v1 != enum_.v2

    def test_similar_eq(self, enum_):
        class TestEnum(compat.Enum):
            v1 = compat.auto()

        assert enum_.v1 != TestEnum.v1

    def test_name(self, enum_):
        assert enum_.v1.name == "v1"

    def test_value(self, enum_):
        assert enum_.v1.value == 1

    def test_repr(self, enum_):
        assert repr(enum_.v1) == f"<{enum_.__name__}.v1: 1>"

    def test_hash(self, enum_):
        assert hash(enum_.v1) == hash(enum_.v1)

    def test_pickle(self, enum_):
        roundtrip = pickle.loads(pickle.dumps(enum_.v1))
        assert roundtrip is enum_.v1


@pytest.mark.parametrize("module", [enum, compat])
def test_unique(module):
    with pytest.raises(ValueError):

        @module.unique
        class Enum(module.Enum):
            answer = 42
            answer_again = 42
