from typing import Union, Optional
from dataclasses import dataclass

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


class Orders():
    orders = {}

    def add(self, order: Union[ClientOrder]):
        self.orders[order.uuid] = order
        pass

    def update(self, order: Union[ClientOrder]):
        self.orders[order.uuid] = order
        pass

    def find_by_id(self, uuid):
        return self.orders[uuid]
