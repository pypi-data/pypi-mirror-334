# Standard library imports
from functools import wraps
from typing import Any, Dict, Callable
from datetime import datetime
from dataclasses import fields, is_dataclass
from datetime import datetime
from enum import Enum
from typing import Callable, Dict
from openai.types.chat import ChatCompletionChunk
def serialize(value: object, remove_null: bool = False, serialization_funcs: Dict[type, Callable] = None, join_list_key = None) -> dict:
    if serialization_funcs:
        for cls, f in serialization_funcs.items():
            if isinstance(value, cls):
                return f(value)
    if isinstance(value, datetime):
        return value.isoformat() + "Z"
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, list):
        if join_list_key is not None:
            value_list = [serialize(v, remove_null, serialization_funcs) for v in value]
            return join_list_key.join(value_list)
        return [serialize(v, remove_null, serialization_funcs) for v in value]
    if isinstance(value, dict):
        return str({k: serialize(v, remove_null, serialization_funcs) for k, v in value.items()})
    if isinstance(value, tuple):
        return tuple(str(v) for v in value)
    if is_dataclass(value):
        if hasattr(value, "serialize"):
            result = value.serialize()
        else:
            result = {
                f.name: serialize(getattr(value, f.name), remove_null, serialization_funcs) for f in fields(value)
            }
        if not remove_null:
            return result
        null_keys = [k for k, v in result.items() if v is None]
        for k in null_keys:
            result.pop(k)
        return result
    try:
        from pydantic import BaseModel

        if isinstance(value, BaseModel):  # Handle pydantic model, which is used in langchain
            return value.dict()
        else:
            return value.json() # Handle ResponseWrapper, which is used in BingGroundingClient
    except Exception:
        pass
    return str(value)

def get_attr(obj: Any, attr: str, default: Any = None) -> Any:
    """Get attribute from either dictionary or object"""
    if isinstance(obj, dict):
        return obj.get(attr, default)
    return getattr(obj, attr, default)

def to_serializable(obj):
    if isinstance(obj, dict) and all(isinstance(k, str) for k in obj.keys()):
        return {k: to_serializable(v) for k, v in obj.items()}
    try:
        obj = serialize(obj)
    except Exception:
        # We don't want to fail the whole function call because of a serialization error,
        # so we simply convert it to str if it cannot be serialized.
        obj = str(obj)
    return obj
