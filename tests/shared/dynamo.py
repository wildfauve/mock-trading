import pytest

from trading.instruction.model import instruction_model as ins_model
from trading.broker.model import broker_order_model as bord_model
from trading.execution.model import market_order_model as mord_model



@pytest.fixture(scope='session', autouse=True)
def dynamo_setup():
    ins_model.create_table()
    bord_model.create_table()
    mord_model.create_table()

    yield

    ins_model.delete_table()
    bord_model.delete_table()
    mord_model.delete_table()