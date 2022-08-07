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

### Benchmarking

If you install the `[benchmark]` extra, you can use
[`richbench`](https://pypi.org/project/richbench/) to see a performance
comparison between `enum` and `basicenum.compat`.

#### Results

On a MacBook Pro (Retina, 13-inch, Early 2015):

```sh
richbench --repeat 5 --times 5 --benchmark compat benchmarks/
```

|                 Benchmark | Min     | Max     | Mean    | Min (+)         | Max (+)         | Mean (+)        |
|---------------------------|---------|---------|---------|-----------------|-----------------|-----------------|
|                    import | 0.374   | 0.503   | 0.422   | 0.117 (3.2x)    | 0.120 (4.2x)    | 0.119 (3.5x)    |
|      creation w/ `auto()` | 0.422   | 0.429   | 0.425   | 0.075 (5.7x)    | 0.077 (5.5x)    | 0.076 (5.6x)    |
| `_generate_next_value_()` | 0.373   | 0.383   | 0.376   | 0.077 (4.8x)    | 0.078 (4.9x)    | 0.078 (4.8x)    |
|     creation w/ constants | 0.333   | 0.351   | 0.339   | 0.060 (5.5x)    | 0.066 (5.4x)    | 0.063 (5.4x)    |
|            functional API | 0.392   | 0.397   | 0.394   | 0.070 (5.6x)    | 0.074 (5.4x)    | 0.072 (5.5x)    |
|     isinstance(..., Enum) | 0.189   | 0.191   | 0.190   | 0.279 (-1.5x)   | 0.282 (-1.5x)   | 0.280 (-1.5x)   |
|              `iter(Enum)` | 0.912   | 0.922   | 0.917   | 0.197 (4.6x)    | 0.199 (4.6x)    | 0.198 (4.6x)    |
|               `Enum(...)` | 0.297   | 0.297   | 0.297   | 0.078 (3.8x)    | 0.079 (3.8x)    | 0.078 (3.8x)    |
|               `Enum[...]` | 0.121   | 0.122   | 0.121   | 0.075 (1.6x)    | 0.139 (-1.1x)   | 0.093 (1.3x)    |
|             `... in Enum` | 0.267   | 0.375   | 0.308   | 0.162 (1.6x)    | 0.164 (2.3x)    | 0.163 (1.9x)    |
|             member access | 0.333   | 0.337   | 0.334   | 0.118 (2.8x)    | 0.121 (2.8x)    | 0.119 (2.8x)    |
|              value access | 0.735   | 0.761   | 0.744   | 0.141 (5.2x)    | 0.143 (5.3x)    | 0.142 (5.2x)    |
|                  equality | 0.343   | 0.345   | 0.344   | 0.103 (3.3x)    | 0.107 (3.2x)    | 0.105 (3.3x)    |
|                      repr | 0.379   | 0.386   | 0.382   | 0.236 (1.6x)    | 0.238 (1.6x)    | 0.237 (1.6x)    |
|                   hashing | 0.345   | 0.355   | 0.348   | 0.245 (1.4x)    | 0.250 (1.4x)    | 0.247 (1.4x)    |
|                  pickling | 0.270   | 0.272   | 0.271   | 0.270 (-1.0x)   | 0.274 (-1.0x)   | 0.272 (-1.0x)   |
|                unpickling | 0.229   | 0.232   | 0.231   | 0.230 (-1.0x)   | 0.232 (-1.0x)   | 0.231 (-1.0x)   |
|             `__members__` | 0.373   | 0.381   | 0.376   | 0.046 (8.1x)    | 0.047 (8.1x)    | 0.046 (8.1x)    |
|                 `@unique` | 0.518   | 0.523   | 0.520   | 0.104 (5.0x)    | 0.109 (4.8x)    | 0.106 (4.9x)    |

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
