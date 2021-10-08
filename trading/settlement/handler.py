from pyfuncify import monad
import uuid

from .domain import ledger

def initiate_client_order_settlement_instruction(ord):
    return monad.Right(ord) >> shadow_client_order


def shadow_client_order(ord):
    shadow = ledger.Order(
        uuid=unique_id(),
        counter_party=ledger.client_cp,
        external_order_origin=ord.uuid,
        order_reference=ord.uuid,
        buy_sell=ord.action,
        market_id="SPK",
        instrument_code="abc",
        qty=ord.qty,
        price=ord.price
    )
    ledger.Orders().add(shadow)
    return monad.Right(shadow.uuid)


def unique_id():
    return str(uuid.uuid4())
