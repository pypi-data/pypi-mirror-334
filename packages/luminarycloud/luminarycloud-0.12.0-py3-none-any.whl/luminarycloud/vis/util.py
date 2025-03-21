from luminarycloud.types import Vector3
from dataclasses import dataclass, field, fields
from typing import List, cast, Type, TypeVar, Callable, Any


def is_list_vec3(obj: list) -> bool:
    if isinstance(obj, list) and len(obj) == 3:
        return all(isinstance(item, (int, float)) for item in obj)
    return False


def convertToVec3(value: list | Vector3) -> Vector3:
    if isinstance(value, Vector3):
        return value
    elif is_list_vec3(value):
        return Vector3(x=value[0], y=value[1], z=value[2])
    else:
        raise TypeError(f"Invalid type for vec3: '{value}'")


T = TypeVar("T")


def vector3_wrapper(cls: Type[T]) -> Type[T]:
    """
    Automatically generates @property and @setter for Vector3 fields.  We use
    vector3 all over the place and this reduces the boilerplate code we need to
    use the helpers.
    """

    def make_property(name: str) -> property:
        private_name = f"_{name}"

        def getter(self: Any) -> Any:
            return getattr(self, private_name)

        def setter(self: Any, value: Vector3 | List) -> None:
            setattr(self, private_name, cast(Vector3, convertToVec3(value)))

        return property(getter, setter)

    for f in fields(cls):
        if f.type is Vector3:
            setattr(cls, f.name, make_property(f.name))  # Properly binds each name

    return cls
