from pyfuncify import monad

from ..venue import handler as venue
from .domain import market_order

def new_order(bord):
    return monad.Right(bord) >> to_new_market_order >> create >> place >> new_order_result

def to_new_market_order(bord):
    mord = market_order.create_new_market_order(bord)
    return monad.Right(mord)


def create(mord):
    market_order.create(mord)
    return monad.Right(mord)

def place(mord):
    venue.placement(mord)
    return monad.Right(mord)

def new_order_result(mord):
    return ('ok', mord.uuid)
