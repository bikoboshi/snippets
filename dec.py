"""
Here are two decorator implementations:
1. Decorator implemented using classes. (Has limitations. Might be a language bug.)
2. Decorator implemented using functions.
"""

from functools import wraps

USE_CLASS_DEFINITION = not True

class Counter:
    def __init__(self, f):
        self._f = f
        self._count = 0

    def __call__(self, *args, **kwargs):
        self._count += 1
        print(f"Count ({self._f.__name__}): {self._count}")
        result = self._f(*args, **kwargs)
        return result

def counter(f):
    count = 0

    @wraps(f)
    def wrapper(*args, **kwargs):
        # Not sure why "count" needs to be declared nonlocal but not "f"
        nonlocal count
        count += 1
        print(f"Count ({f.__name__}): {count}")
        result = f(*args, **kwargs)
        return result
    return wrapper

count_decorator = Counter if USE_CLASS_DEFINITION else counter

def each_instance(dec):
    def decorator(f):
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            # User needs to be aware that their instance namespace will be used.
            if not hasattr(self, '_each_instance_dec'):
                self._each_instance_dec = dec(f)
            result = self._each_instance_dec(self, *args, **kwargs)
            return result
        return wrapper
    return decorator

class Summer:
    @count_decorator
    def __call__(self, *args, **kwargs):
        return sum(*args)

    @count_decorator
    def sum1(self, *args, **kwargs):
        return sum(*args)

    @each_instance(count_decorator)
    def sum2(self, *args, **kwargs):
        return sum(*args)

s = Summer()
arr = [1,2,3,4,5]
ans = sum(arr)

try:
    # Expectation for both decorators
    assert(s(arr) == ans)
except TypeError as e:
    print(e)
    # Workaround for class definition
    assert(s(s, arr) == ans)
    
try:
    # Expectation for both decorators
    assert(s.sum1(arr) == ans)
except TypeError as e:
    print(e)
    # Workaround for class definition
    assert(s.sum1(s, arr) == ans)

if not USE_CLASS_DEFINITION:
    s1 = Summer()
    s2 = Summer()
    print("Each instance:")
    s1.sum2(arr) # 1
    s2.sum2(arr) # 1
    s1.sum2(arr) # 2
    s2.sum2(arr) # 2
    s2.sum2(arr) # 3
    s2.sum2(arr) # 4
    s1.sum2(arr) # 3
    s1.sum2(arr) # 4
