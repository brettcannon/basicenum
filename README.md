# basicenum

Simple(r) enums.

## `basicenum.compat`

A (mostly) API-compatible re-implementation of `enum.Enum` from the stdlib
(plus related code).

The goal for this module was to try and re-implement as much of the API of
`enum.Enum` as possible while using modern Python features. While this does lead
to some API breakage (e.g. `type(enum.member) == type(enum)` is no longer true),
it mostly revolves around metaclass-level details. If you rely on the surface
API for `enum.Enum`, then this module should be compatible.

### API Compatibility

Using the example enum:

```python
class Colour(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()
```

The compatibility with `enum.Enum` is:

| Feature | Supported? |
| ------- | ---------- |
|`repr(Colour.RED)`|✅|
|`type(Colour.RED)`|❌ (`Member` instead)|
|`isinstance(Colour.RED, Colour)`|✅|
|`iter(Colour)`|✅|
|`hash(Colour.RED)`|✅|
|`Colour(1)`|✅|
|`Colour["RED"]`|✅|
|`Colour.RED in Colour`|✅|
|`Colour.RED.name`|✅|
|`Colour.RED.value`|✅|
|`auto()`|✅|
|`_generate_next_value_()`|✅|
|`Colour.__members__`|✅|
|`Colour.RED == Colour.RED`|✅|
|Restricted subclassing|❌|
|Pickling|✅|
|Functional API|✅ (via `create()`)|

### Type Checking

Unfortunately, type checkers hard-code their support for `enum.Enum`. That means
they do not recognize members of `basicenum.compat.Enum` as being instances of
`Member` or matching the API of members of `enum.Enum`. Auto-complete based on
member names should work, though.

### Module Contents

#### `Enum`

The class to inherit from to create an enum.

#### `Member`

The class which all enum members are instances of.

#### `auto()`

Function for automatic, incrementing integer member values.

#### `@unique`

Guarantee that all enum members have unique values.

Raises `ValueError` if values are not all unique.

#### `create()`

A re-implementation of the functional API of `enum.Enum`.

```python
def create(
    enum_name, member_names, /, *, module=None, qualname=None, type=None, start=1
): ...
```
