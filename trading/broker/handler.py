from pyfuncify import monad
from pymonad.reader import Pipe
import uuid

from .domain import broker_order
from ..settlement import handler as settlement_service
from ..execution import handler as execution_service

def event_instruction_submitted(ins):
    return  monad.Right(ins) >> \
            create_client_order >> \
            prepare_for_settlement >> \
            release_client_order >> \
            place >> \
            update_bord_to_placing >> \
            return_cord_id_result


def create_client_order(ins):
    cord = broker_order.create_client_order(ins)
    return monad.Right(cord)


def prepare_for_settlement(cord):
    shadow_order_result = settlement_service.initiate_client_order_settlement_instruction(cord)
    broker_order.add_shadow_order_id(cord, shadow_order_result.value)
    return monad.Right(cord)

def release_client_order(cord):
    """
    Allocate a Client Order to a Broker Order.  In this case we do this 1..1
    with no transformation of the cord reference data
    """
    bord = broker_order.release(cord)
    return monad.Right(bord)

def place(bord):
    result = execution_service.new_order(bord)
    broker_order.add_mord_id_to_bord(bord=bord, mord_uuid=result[1])
    return monad.Right(bord)

def update_bord_to_placing(bord):
    broker_order.state_transition_bord_to_placing(bord)
    return monad.Right(bord)

def return_cord_id_result(bord):
    return ('ok', bord.cord_uuid)