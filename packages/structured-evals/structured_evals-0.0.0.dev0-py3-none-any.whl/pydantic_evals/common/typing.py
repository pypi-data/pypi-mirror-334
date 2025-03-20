from enum import Enum
from typing import Annotated, Any, Dict, List, Tuple, Type, Union, get_args, get_origin

from pydantic import BaseModel

try:
    from types import UnionType  # Python 3.10+ (int | None)
except ImportError:
    # If running on Python < 3.10, we define a fallback
    UnionType = ()


def is_union_type(tp: Any) -> bool:
    """
    Return True if tp is a union, in either the old typing.Union or the new types.UnionType style.
    """
    # get_origin() might be <class 'typing.Union'> in py < 3.10, or None in 3.10+ if it's a UnionType
    origin = get_origin(tp)
    return (origin is UnionType) or (origin is __import__("typing").Union)


def get_union_args(tp: Any) -> tuple:
    """
    Return the arguments of a union. In Python 3.10+, int | float sets origin=None,
    so we rely on get_args(...) anyway to return (int, float).
    """
    return get_args(tp)


def is_optional_union(tp: Any) -> bool:
    """
    Check if tp is basically 'Optional[T]' or 'T | None' for exactly one T.
    i.e. a union with exactly 2 args, one of which is NoneType.
    """
    if not is_union_type(tp):
        return False
    args = get_union_args(tp)
    # e.g. (int, NoneType) or (NoneType, int)
    return len(args) == 2 and type(None) in args


def is_list_type(tp: Any) -> bool:
    """Check if tp is a list type"""
    return get_origin(tp) is list


def is_tuple_type(tp: Any) -> bool:
    """Check if tp is a tuple type"""
    return get_origin(tp) is tuple


def type_to_str(tp: Any) -> str:
    """
    Convert a Python type annotation to a string, e.g.:
      int -> 'int'
      list[str] -> 'list[str]'
      Optional[float] -> 'Optional[float]'
      dict[str, int] -> 'dict[str,int]'
    """
    origin = get_origin(tp)
    if origin is None:
        if tp is type(None):
            return "None"
        elif isinstance(tp, str):
            return f"'{tp}'"  # Handle string literals
        else:
            return getattr(tp, "__name__", str(tp))

    # 1) If it's a new UnionType in Python 3.10+, or old typing.Union
    #    get_origin(int | None) == None in 3.10, so we check is_union_type
    if is_union_type(tp):
        args = get_union_args(tp)
        # e.g. (int, NoneType) => Optional[int]
        # e.g. (int, float) => Union[int,float]
        if is_optional_union(tp):
            non_none = next(a for a in args if a is not type(None))
            return f"Optional[{type_to_str(non_none)}]"
        # otherwise a multi-type union
        joined = ",".join(type_to_str(a) for a in args)
        return f"Union[{joined}]"

    if origin in (list, dict, set, tuple):
        args = get_args(tp)
        if not args:
            return origin.__name__  # e.g. "list"
        inner = ",".join(type_to_str(a) for a in args)
        return f"{origin.__name__}[{inner}]"

    # Fallback for other generics
    args = get_args(tp)
    joined = ",".join(type_to_str(a) for a in args)
    
    # Handle Literal types which don't have __name__ in Python 3.9
    if str(origin).startswith('typing.Literal'):
        return f"Literal[{joined}]"
    
    # Handle other generic types
    return f"{getattr(origin, '__name__', str(origin))}[{joined}]"


def is_pydantic_model(t: Type[Any]) -> bool:
    """Check if a type is a Pydantic model"""
    try:
        return issubclass(t, BaseModel)
    except Exception:
        return False


def resolve_complex_type(tp: Any) -> Any:
    """
    Resolves a complex type to its base type, handling Unions, Optional, and nested types.

    Examples:
        Optional[int] -> int
        list[str] -> str
        Union[int, str, None] -> Union[int, str]
        Optional[List[Table]] -> List[Table]
    """
    origin = get_origin(tp)
    if origin is None:
        return tp

    tp_args = get_args(tp)
    if is_union_type(tp):
        # If it's a model type in a union, keep the union structure
        if any(isinstance(arg, type) and is_pydantic_model(arg) for arg in tp_args):
            return tp
        # Get first non-None type for Optional/Union
        inner_type = next(arg for arg in tp_args if arg is not type(None))
        return resolve_complex_type(inner_type)
    elif origin is Annotated:
        return resolve_complex_type(tp_args[0])
    elif origin in (list, List):
        return resolve_complex_type(tp_args[0])
    else:
        return tp


def is_model_or_enum(tp: Any) -> bool:
    """
    Check if a type is either a Pydantic model or an Enum.

    Examples:
        is_model_or_enum(MyModel) -> True
        is_model_or_enum(MyEnum) -> True
        is_model_or_enum(int) -> False
    """
    try:
        return isinstance(tp, type) and (issubclass(tp, BaseModel) or issubclass(tp, Enum))
    except TypeError:
        return False


def get_non_none_type(tp: Any) -> Any:
    """
    Get the non-None type from an Optional/Union type.
    If the type is not a Union/Optional, returns the type as is.

    Examples:
        get_non_none_type(Optional[int]) -> int
        get_non_none_type(Union[str, None]) -> str
        get_non_none_type(int) -> int
    """
    if not is_union_type(tp):
        return tp

    args = get_union_args(tp)
    return next(arg for arg in args if arg is not type(None))
