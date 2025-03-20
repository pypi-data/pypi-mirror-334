"""
Test the staticfunc decorator
"""

from ._staticfunc import staticfunc

class TestStaticFunc:
    """Test the staticfunc decorator"""

    def test_correct_decl(self):
        """Test that the function is declared correctly"""
        @staticfunc()
        def func(a: int, b: float) -> float:
            return a + b
        assert func(1, 2.0) == 3.0

    def test_bad_typing(self):
        """Test that the function must be fully typed"""
        try:
            @staticfunc()
            def func(a, b: float) -> float: # type: ignore
                return a + b # type: ignore
            assert False
        except TypeError as e:
            assert str(e) == "Function must be fully typed!"

    def test_no_casting(self):
        """Test that the function is not casted"""
        try:
            @staticfunc()
            def func(a: int, b: float) -> float:
                return a + b
            func("1", 2.0)
            assert False
        except TypeError as e:
            assert str(e) == "Expected <class 'int'>, got <class 'str'>"

    def test_casting(self):
        """Test that the function is casted correctly"""
        try:
            @staticfunc(cast=True)
            def func(a: int, b: float) -> float:
                return a + b
            assert func("1", 2.0) == 3.0
        except TypeError as _:
            assert False

    def test_no_return(self):
        """Test that the function must have a return type"""
        try:
            @staticfunc()
            def func(a: int, b: float): # type: ignore
                return a + b

            assert False
        except TypeError as e:
            assert str(e) == "Function must have a return type!"

    def test_no_return_casting(self):
        """Test that the return type is not casted"""
        try:
            @staticfunc()
            def func(a: int, b: int) -> float:
                return a + b
            func(1, 2)
            assert False
        except TypeError as e:
            assert str(e) == "Expected <class 'float'>, got <class 'int'>"

    def test_return_casting(self):
        """Test that the return type is casted"""
        try:
            @staticfunc(cast=True)
            def func(a: int, b: int) -> float:
                return a + b
            assert func(1, 2) == 3.0
        except TypeError as _:
            assert False
