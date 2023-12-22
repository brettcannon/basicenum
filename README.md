# basicenum

Simple(r) enums.

## `basicenum.compat`

A (mostly) API-compatible re-implementation of
[`enum.Enum`](https://docs.python.org/3/library/enum.html#enum.Enum) from the
stdlib (plus related code).

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
|`str(Colour.RED)`|✅|
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
`Member` or matching the API of members of `enum.Enum`.

Luckily, you can lie to the type checkers. You can tell them to type check as if
you're using `enum` while using `basicenum.compat` during execution.

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from enum import Enum, auto
else:
    from basicenum.compat import Enum, auto
```

### Benchmarking

If you install the `[benchmark]` extra, you can use
[`richbench`](https://pypi.org/project/richbench/) to see a performance
comparison between `enum` and `basicenum.compat`.

#### Results

Using a AMD Ryzen™ 7 7840U w/ Radeon™ 780M Graphics × 16 w/ Python 3.12.1:

```sh
richbench --markdown --repeat 5 --times 5 --benchmark compat benchmarks/
```
                                         Benchmarks, repeat=5, number=5

|                 Benchmark | Min     | Max     | Mean    | Min (+)         | Max (+)         | Mean (+)        |
|---------------------------|---------|---------|---------|-----------------|-----------------|-----------------|
|                    import | 0.411   | 0.416   | 0.413   | 0.041 (10.1x)   | 0.050 (8.3x)    | 0.043 (9.5x)    |
|      creation w/ `auto()` | 0.221   | 0.225   | 0.223   | 0.046 (4.8x)    | 0.047 (4.8x)    | 0.046 (4.8x)    |
| `_generate_next_value_()` | 0.184   | 0.186   | 0.185   | 0.053 (3.5x)    | 0.053 (3.5x)    | 0.053 (3.5x)    |
|     creation w/ constants | 0.156   | 0.157   | 0.157   | 0.041 (3.8x)    | 0.042 (3.8x)    | 0.041 (3.8x)    |
|            functional API | 0.181   | 0.183   | 0.182   | 0.042 (4.3x)    | 0.043 (4.2x)    | 0.043 (4.3x)    |
|     isinstance(..., Enum) | 0.039   | 0.039   | 0.039   | 0.119 (-3.1x)   | 0.121 (-3.1x)   | 0.120 (-3.1x)   |
|              `iter(Enum)` | 0.282   | 0.284   | 0.283   | 0.094 (3.0x)    | 0.096 (3.0x)    | 0.095 (3.0x)    |
|               `Enum(...)` | 0.109   | 0.110   | 0.110   | 0.053 (2.1x)    | 0.055 (2.0x)    | 0.053 (2.1x)    |
|               `Enum[...]` | 0.025   | 0.026   | 0.026   | 0.025 (1.0x)    | 0.027 (-1.1x)   | 0.026 (-1.0x)   |
|             `... in Enum` | 0.036   | 0.036   | 0.036   | 0.068 (-1.9x)   | 0.069 (-1.9x)   | 0.068 (-1.9x)   |
|             member access | 0.066   | 0.068   | 0.067   | 0.067 (-1.0x)   | 0.067 (1.0x)    | 0.067 (-1.0x)   |
|              value access | 0.225   | 0.230   | 0.228   | 0.044 (5.1x)    | 0.044 (5.2x)    | 0.044 (5.2x)    |
|                  equality | 0.064   | 0.064   | 0.064   | 0.063 (1.0x)    | 0.064 (-1.0x)   | 0.064 (1.0x)    |
|                      repr | 0.118   | 0.119   | 0.118   | 0.093 (1.3x)    | 0.093 (1.3x)    | 0.093 (1.3x)    |
|                       str | 0.067   | 0.067   | 0.067   | 0.061 (1.1x)    | 0.061 (1.1x)    | 0.061 (1.1x)    |
|                   hashing | 0.103   | 0.103   | 0.103   | 0.103 (-1.0x)   | 0.104 (-1.0x)   | 0.103 (-1.0x)   |
|                  pickling | 0.113   | 0.114   | 0.114   | 0.113 (1.0x)    | 0.113 (1.0x)    | 0.113 (1.0x)    |
|                unpickling | 0.109   | 0.111   | 0.109   | 0.109 (1.0x)    | 0.109 (1.0x)    | 0.109 (1.0x)    |
|             `__members__` | 0.126   | 0.128   | 0.127   | 0.027 (4.7x)    | 0.028 (4.5x)    | 0.027 (4.7x)    |
|                 `@unique` | 0.270   | 0.274   | 0.273   | 0.058 (4.7x)    | 0.061 (4.5x)    | 0.059 (4.6x)    |


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
