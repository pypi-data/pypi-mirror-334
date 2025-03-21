from composable import pipeable
from typing import Optional, TypeVar, Callable

A = TypeVar('A')
B = TypeVar('B')


@pipeable
def with_default(default: A, arg: Optional[A]) -> A:
    ''' Provide a default value, turning an optional value into a normal value.

    Args:
        - default: Default to replace `None`
        - opt: argument of type Optional[A]
    
    Returns: arg when arg is not None else default
    >>> from composable.maybe import withDefault
    >>> None >> with_default('a')
    'a'
    >>> 'b' >> with_default('a')
    'b'
    '''
    return default if arg is None else arg


@pipeable
def map(f: Callable[[A], B], arg: Optional[A]) -> Optional[B]:
    ''' Transform an optional value with a function.

    Args:
        - f: function
        - arg: optional value

    Returns: f(arg) if arg is not None else None

    Examples:

    >>> from composable import maybe
    >>> from toolz.curried.operator import add
    >>> None >> maybe.map(add(2))
    >>> None >> maybe.map(add(2)) is None
    True
    >>> 3 >> maybe.map(add(2))
    5
    >>> from composable.strict import map
    >>> [1,2,None,4] >> map(maybe.map(add(2)))
    [3, 4, None, 6]
    ''' 
    return f(arg) if arg is not None else None