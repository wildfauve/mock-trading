from typing import Union, Optional
import uuid
from dataclasses import dataclass

from ..model import broker_order_model as model

@dataclass
class FinancialProduct():
    id: str
    jurisdiction: str


@dataclass
class PriceCurrency():
    price: str
    currency: str

@dataclass
class DefaultSettlementInstruction():
    shadow_order_id: Optional[str]
    pass


@dataclass
class ClientOrder:
    uuid: str
    instruction_uuid: str
    action: str
    trading_client: str
    settlement_instructions: DefaultSettlementInstruction
    financial_product: FinancialProduct
    order_type: str
    qty: int
    price: PriceCurrency
    state: str
    repo: Optional[model.ClientOrder] = None


@dataclass
class BrokerOrder:
    uuid: str
    cord_uuid: str
    action: str
    trading_client: str
    financial_product: FinancialProduct
    order_type: str
    qty: int
    price: PriceCurrency
    state: str
    repo: Optional[model.BrokerOrder] = None

def create_client_order(ins):
    fp = FinancialProduct(id=ins.instruction['financialProduct']['id'],
                          jurisdiction=ins.instruction['financialProduct']['tradingJurisdiction'])
    price = PriceCurrency(price=ins.instruction['strategy']['price']['price'],
                          currency=ins.instruction['strategy']['price']['priceCurrency'])
    cord = ClientOrder(financial_product=fp,
                       instruction_uuid=ins.uuid,
                       action=ins.instruction['action'],
                       settlement_instructions=DefaultSettlementInstruction(shadow_order_id=None),
                       uuid=unique_id(),
                       trading_client=ins.instruction['instructingParties']['tradingParty']['id'],
                       order_type=ins.instruction['strategy']['execution'],
                       qty=ins.instruction['strategy']['qty']['value'],
                       price=price,
                       state='created')
    repo = save_client_order(cord)
    cord.repo = repo
    return cord

def release(cord):
    bord = BrokerOrder(financial_product=cord.financial_product,
                        cord_uuid=cord.uuid,
                        action=cord.action,
                        uuid=unique_id(),
                        trading_client=cord.trading_client,
                        order_type=cord.order_type,
                        qty=cord.qty,
                        price=cord.price,
                        state="placeable")
    bord.repo = save_broker_order(bord)
    return bord


def add_shadow_order_id(cord, shadow_order_id):
    cord.settlement_instructions.shadow_order_id = shadow_order_id
    cord.repo.settlement_instructions.shadow_order_id = shadow_order_id
    cord.repo.save()
    return cord

def add_mord_id_to_bord(bord, mord_uuid):
    bord.mord_uuid = mord_uuid
    bord.repo.mord_uuid = mord_uuid
    bord.repo.save()
    return bord

def state_transition_bord_to_placing(bord):
    bord.state = "placing"
    bord.repo.state = "placing"
    bord.repo.save()
    return bord


def save_client_order(cord: ClientOrder):
    repo = model.ClientOrder(hash_key=cord_pk(cord.uuid),
                             range_key=meta_sk(cord.uuid),
                             uuid=cord.uuid,
                             ins_uuid= cord.instruction_uuid,
                             action=cord.action,
                             trading_client=cord.trading_client,
                             order_type=cord.order_type,
                             settlement_instructions=model.SettlementInstruction(),
                             financial_product=model.FinancialProduct(id=cord.financial_product.id,
                                                                      jursidiction=cord.financial_product.jurisdiction),
                             price=model.Price(price=cord.price.price, currency=cord.price.currency),
                             qty=cord.qty,
                             state=cord.state)
    repo.save()
    return repo

def save_broker_order(bord: BrokerOrder):
    repo = model.BrokerOrder(hash_key=bord_pk(bord.uuid),
                             range_key=meta_sk(bord.uuid),
                             uuid=bord.uuid,
                             cord_uuid=bord.cord_uuid,
                             action=bord.action,
                             trading_client=bord.trading_client,
                             order_type=bord.order_type,
                             settlement_instructions=model.SettlementInstruction(),
                             financial_product=model.FinancialProduct(id=bord.financial_product.id,
                                                                      jursidiction=bord.financial_product.jurisdiction),
                             price=model.Price(price=bord.price.price, currency=bord.price.currency),
                             qty=bord.qty,
                             state=bord.state)
    repo.save()
    return repo

def cord_pk(uuid):
    return "CORD#{}".format(uuid)


def bord_pk(uuid):
    return "BORD#{}".format(uuid)


def meta_sk(uuid):
    return "META#{}".format(uuid)


def unique_id():
    return str(uuid.uuid4())
