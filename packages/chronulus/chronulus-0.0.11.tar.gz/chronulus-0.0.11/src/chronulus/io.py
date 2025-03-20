import sys
from pydantic import BaseModel

def get_deep_size_bytes(obj) -> int:
    """Get a more comprehensive size for complex objects"""
    if isinstance(obj, (str, bytes, int, float, bool, type(None))):
        return sys.getsizeof(obj)

    size = sys.getsizeof(obj)
    if issubclass(obj.__class__, BaseModel) or isinstance(obj, BaseModel):
        obj = obj.model_dump()

    if isinstance(obj, dict):
        size += sum(get_deep_size_bytes(k) + get_deep_size_bytes(v) for k, v in obj.items())
    elif isinstance(obj, (list, tuple, set)):
        size += sum(get_deep_size_bytes(i) for i in obj)

    return size


def get_object_size_mb(obj) -> float:
    # Get object size in bytes
    size_in_bytes = get_deep_size_bytes(obj)
    # Convert to mb
    size_in_mb = size_in_bytes / (1024 * 1024)
    return size_in_mb