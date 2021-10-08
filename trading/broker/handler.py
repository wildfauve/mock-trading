from pyfuncify import monad
import uuid

from .domain import order
from ..settlement import handler as settlement_service
from ..execution import handler as execution_service

def submitted_event(ins):
    result = monad.Right(ins) >> create_client_order >> prepare_for_settlement >> allocate >> place
    breakpoint()
    pass

def create_client_order(ins):
    fp = order.FinancialProduct(id=ins.instruction['financialProduct']['id'],
                                jurisdiction=ins.instruction['financialProduct']['tradingJurisdiction'])
    price = order.PriceCurrency(price=ins.instruction['strategy']['price']['price'],
                                currency=ins.instruction['strategy']['price']['priceCurrency'])
    cord = order.ClientOrder(financial_product=fp,
                             instruction_uuid=ins.uuid,
                             action=ins.instruction['action'],
                             settlement_instructions=order.DefaultSettlementInstruction(shadow_order_id=None),
                             uuid=unique_id(),
                             trading_client=ins.instruction['instructingParties']['tradingParty']['id'],
                             order_type=ins.instruction['strategy']['execution'],
                             qty=ins.instruction['strategy']['qty']['value'],
                             price=price)
    order.Orders().add(cord)
    return monad.Right(cord)


def prepare_for_settlement(ord):
    result = settlement_service.initiate_client_order_settlement_instruction(ord)
    ord.settlement_instructions.shadow_order_id = result.value
    order.Orders().update(ord)
    return monad.Right(ord)

def allocate(cord):
    """
    Allocate a Client Order to a Broker Order.  In this case we do this 1..1
    with no transformation of the cord reference data
    """
    bord = order.BrokerOrder(financial_product=cord.financial_product,
                             cord_uuid=cord.uuid,
                             action=cord.action,
                             uuid=unique_id(),
                             trading_client=cord.trading_client,
                             order_type=cord.order_type,
                             qty=cord.qty,
                             price=cord.price)
    order.Orders().add(bord)
    return monad.Right(bord)

def place(bord):
    result = execution_service.new_order(bord)
    breakpoint()

def unique_id():
    return str(uuid.uuid4())
