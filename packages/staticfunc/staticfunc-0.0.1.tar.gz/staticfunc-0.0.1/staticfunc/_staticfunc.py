"""
Static type checking for functions in Python.
"""

from typing import Any, Callable, Dict, List

def staticfunc(cast: bool = False) -> Callable[..., Any]:
    """Static Function Wrapper"""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        if not func.__annotations__:
            raise TypeError("Function must be fully typed!")
        if "return" not in func.__annotations__:
            raise TypeError("Function must have a return type!")
        for key in func.__annotations__:
            if key == "return":
                continue
            if not func.__annotations__[key]:
                raise TypeError("Function must be fully typed!")
            if func.__code__.co_argcount != len(func.__annotations__)-1:
                raise TypeError("Function must be fully typed!")

        arg_count = func.__code__.co_argcount

        def wrapper(*_args: Any, **kwargs: Dict[Any, Any]) -> Any:
            annotations = func.__annotations__
            args: List[Any] = list(_args)
            if len(args) != arg_count:
                raise TypeError(f"Expected {arg_count} arguments, got {len(args)}")
            for i, arg in enumerate(args):
                if not isinstance(arg, annotations[list(annotations.keys())[i]]):
                    if cast:
                        try:
                            args[i] = annotations[list(annotations.keys())[i]](arg)
                        except Exception as e:
                            raise TypeError(
                            f"Expected {annotations[list(annotations.keys())[i]]}, got {type(arg)}"
                            ) from e
                    else:
                        raise TypeError(
                            f"Expected {annotations[list(annotations.keys())[i]]}, got {type(arg)}")
            result: Any = func(*args, **kwargs)
            if not isinstance(result, annotations["return"]):
                if cast:
                    try:
                        result = annotations["return"](result)
                    except Exception as e:
                        raise TypeError(
                            f"Expected {annotations['return']}, got {type(result)}"
                        ) from e
                else:
                    raise TypeError(f"Expected {annotations['return']}, got {type(result)}")
            return result
        return wrapper
    return decorator
