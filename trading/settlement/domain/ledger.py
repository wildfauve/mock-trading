from dataclasses import dataclass

class Ledger:
    def __init__(self, name):
        self.name = name
        pass

class Transaction:
    pass

@dataclass
class PriceCurrency():
    price: str
    currency: str

@dataclass
class CounterParty:
    code: str


@dataclass
class Order():
    uuid: str
    external_order_origin: str
    order_reference: str
    buy_sell: str
    market_id: str
    instrument_code: str
    qty: int
    price: PriceCurrency
    counter_party: CounterParty

class Orders():
    orders = {}

    def add(self, order: Order):
        self.orders[order.uuid] = order
        pass

    def find_by_id(self, uuid):
        return self.orders[uuid]



market_trade_ledger = Ledger(name="MarketTrade")
pool_contra = Ledger(name="PoolContra")
client_trade_ledger = Ledger(name="ClientTrade")

client_cp = CounterParty(code="trading_client_1")
agent_broker_cp = CounterParty(code="ubs_global")