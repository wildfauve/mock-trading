from pyfuncify import monad

from .domain import fix


def new_order(bord):
    result = monad.Right(bord) >> to_fix >> place
    breakpoint()

def to_fix(bord):
    t1 = fix.Tag(name='SecurityID', value='abc')
    breakpoint()