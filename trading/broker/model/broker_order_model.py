from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute, MapAttribute, ListAttribute,DiscriminatorAttribute
)

class SettlementInstruction(MapAttribute):
    shadow_order_id = UnicodeAttribute(null=True)

class FinancialProduct(MapAttribute):
    id = UnicodeAttribute(null=False)
    jursidiction = UnicodeAttribute(null=False)

class Price(MapAttribute):
    price = UnicodeAttribute(null=False)
    currency = UnicodeAttribute(null=False)


class BaseModel(Model):
    """
    Base Model consisting of the single table convention; the hash and range keys named PK and SK respectively.
    """
    class Meta:#(Model.Meta):
        table_name = "broker"
        host = "http://localhost:8000"
        write_capacity_units = 1
        read_capacity_units = 1
    PK = UnicodeAttribute(hash_key=True)
    SK = UnicodeAttribute(range_key=True)
    kind = DiscriminatorAttribute()


class ClientOrder(BaseModel, discriminator='client_order'):
    uuid = UnicodeAttribute()
    state = UnicodeAttribute()
    ins_uuid = UnicodeAttribute()
    action = UnicodeAttribute()
    trading_client = UnicodeAttribute()
    order_type = UnicodeAttribute()
    qty = NumberAttribute()
    settlement_instructions = MapAttribute(of=SettlementInstruction)
    financial_product = MapAttribute(of=FinancialProduct)
    price = MapAttribute(of=Price)
    state = UnicodeAttribute()


class BrokerOrder(BaseModel, discriminator='broker_order'):
    uuid = UnicodeAttribute()
    state = UnicodeAttribute()
    cord_uuid = UnicodeAttribute()
    mord_uuid = UnicodeAttribute(null=True)
    action = UnicodeAttribute()
    trading_client = UnicodeAttribute()
    order_type = UnicodeAttribute()
    qty = NumberAttribute()
    settlement_instructions = MapAttribute(of=SettlementInstruction)
    financial_product = MapAttribute(of=FinancialProduct)
    price = MapAttribute(of=Price)
    state = UnicodeAttribute()


def delete_table():
    BaseModel.delete_table()
    ...

def create_table():
    if not BaseModel.exists():
        BaseModel.create_table()
    ...
