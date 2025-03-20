"""
Static Function Wrapper

Checks types of the function and ensures that the function is 
called with the correct types before calling the function.

Also checks the return type of the function.
If cast is disabled, the function will raise an error if the types are incorrect.

If cast is enabled, the function will attempt to cast the types to the 
correct types before calling the function.

Usage:
@staticfunc(cast=false)
def test_func(a: int, b: float) -> float:
    return a + b
"""

from ._staticfunc import staticfunc

__all__ = ["staticfunc"]
__version__ = "0.1.0"
