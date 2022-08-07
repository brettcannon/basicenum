"""An API-compatible re-implementation of `enum.Enum` and related code."""
import collections.abc
import functools
import types

_AUTO = object()


# XXX Make generic
class Member:

    """Representation of an enum member."""

    # The class overall tries to preserve object identity for fast object
    # comparison.

    def __init__(self, cls, name, value):
        self._cls = cls
        self.name = name
        self.value = value

    # Could also use __getnewargs(_ex)__, but this was the simplest solution.
    def __reduce__(self):
        """Pickle by specifying the containing class and name of the member.

        Unpickling retains object identity.

        """
        return getattr, (self._cls, self.name)

    def __repr__(self):
        return f"<{self._cls.__name__}.{self.name}: {self.value!r}>"

    def __hash__(self):
        """Hash the name of the member.

        This matches the semantics of the `enum` module from the stdlib.

        """
        return hash(self.name)


def auto():
    """Specify that the member should be an auto-incremented int."""
    return _AUTO


class Meta(type):

    """An API-compatible re-implementation of `enum.EnumMeta`."""

    def __new__(meta, name, bases, ns):
        """Convert class attributes to enum members."""
        cls = super().__new__(meta, name, bases, ns)
        members = {}
        last_auto = 0
        if (custom_auto := ns.get("_generate_next_value_")) is None:
            for base in bases:
                if hasattr(base, "_generate_next_value_"):
                    custom_auto = base._generate_next_value_
                    break
        # The rules in `enum` are much more strict in what gets skipped.
        # Need to do this upfront so enumerate() returns what's expected for
        # _generate_next_value_().
        members_iter = (
            (name, value)
            for name, value in ns.items()
            if not isinstance(value, types.FunctionType) and not name.startswith("_")
        )
        for index, (name, value) in enumerate(members_iter):
            if value is _AUTO:
                if custom_auto is None:
                    last_auto += 1
                    value = last_auto
                else:
                    value = custom_auto(
                        name,
                        1,  # No way to specified a different starting value.
                        index,
                        list(member.value for member in members.values()),
                    )
            elif isinstance(value, int):
                last_auto = value
            member = Member(cls, name, value)
            members[name] = member
            setattr(cls, name, member)
        cls.__members__ = members

        return cls

    def __instancecheck__(self, ins, /):
        """Check if a member belongs to the enum."""
        return getattr(ins, "_cls", None) is self

    def __iter__(self):
        """Iterator through the members."""
        return iter(self.__members__.values())

    # Memoize to avoid having to store an inverted __members__ dict or deal with
    # values that cannot be hashed.
    @functools.cache
    def __call__(self, value, /):
        """Search members by value."""
        for member in self:
            if member.value == value:
                return member
        else:
            raise ValueError(f"no enum member with a value of {value!r}")

    def __getitem__(self, name, /):
        """Search by member name."""
        return self.__members__[name]

    def __contains__(self, other, /):
        """Check if the argument is a member or value of the enum."""
        return self.__instancecheck__(other)


class Enum(metaclass=Meta):

    """An API-compatible re-implementation of `enum.Enum`."""


def _set_names(ns, qualname, module, name):
    """Set various names in the namespace."""
    if qualname is not None:
        ns["__qualname__"] = qualname
    elif module is not None:
        ns["__qualname__"] = f"{module}.{name}"
    else:
        ns["__qualname__"] = name
    ns["__module__"] = module or None


def create(
    enum_name, member_names, /, *, module=None, qualname=None, type=None, start=1
):
    """Create an enum using the equivalent functional API for `enum.Enum`."""
    if isinstance(member_names, str):
        ns = {
            name: index
            for index, name in enumerate(
                member_names.replace(",", " ").split(), start=start
            )
        }
    elif not isinstance(member_names, collections.abc.Mapping):
        names_seq = list(member_names)
        if names_seq:
            if isinstance(names_seq[0], str):
                ns = {name: index for index, name in enumerate(names_seq, start=start)}
            else:
                ns = dict(names_seq)
        else:
            ns = {}
    else:
        ns = member_names

    _set_names(ns, qualname, module, enum_name)

    if type:
        bases = (type,)
    else:
        bases = ()

    return Meta(enum_name, bases, ns)


def unique(cls):
    """Make sure all enum members have unique values.

    Raises ValueError if any duplicate values are found.

    """
    seen = []
    for value in (member.value for member in cls.__members__.values()):
        if value in seen:
            raise ValueError(f"{cls!r} enum reused {value!r}")
        else:
            seen.append(value)
    else:
        return cls
