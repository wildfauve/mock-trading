from dataclasses import dataclass
import uuid
from pyfuncify import fn
from pymonad.tools import curry

from . import fix
from ..model import market_order_model as model

@dataclass
class NewOrderSingle():
    uuid: str
    tags: dict
    state: str

def create_new_market_order(bord):
    return fix.NewOrderSingle(uuid=unique_id(),
                              state='created',
                              tags=order_tags(bord))

def order_tags(bord):
    return [
        fix.Tag(name='SecurityID', value=bord.financial_product.id),
        fix.Tag(name='SecurityIDSource', value="BLAH"),
        fix.Tag(name='Account', value="R"), # retail
        fix.Tag(name='OrdType', value=bord.order_type),
        fix.Tag(name='Price', value=bord.price.price),
        fix.Tag(name='Side', value=to_side(bord.action)),
        fix.Tag(name='TimeInForce', value="GoodTillDate"),
        fix.Tag(name='ExpiryDate', value="01-01-2022"),
        fix.Tag(name='ClOrdID', value=bord.cord_uuid),
        fix.Tag(name='OrderQty', value=bord.qty),
        fix.Tag(name='TransactTime', value="2021-10-12 09:00:00.000"),
        fix.Tag(name='NoPartyIDs', value=3),
        fix.Tag(name='PartyID', value="CSN-id"),
        fix.Tag(name='PartyIDSource', value='GenerallyAcceptedMarketParticipantIdentifier'),
        fix.Tag(name='PartyRole', value='InvesterId'),
        fix.Tag(name='PartyID', value='blah-blah'),
        fix.Tag(name='PartyIDSource', value='GenerallyAcceptedMarketParticipantIdentifier'),
        fix.Tag(name='PartyRole', value='ClientId'),
        fix.Tag(name='PartyID', value='DMAClient'),
        fix.Tag(name='PartyIDSource', value='GenerallyAcceptedMarketParticipantIdentifier'),
        fix.Tag(name='PartyRole', value='OrderEntryOperatorId')
    ]

def to_side(action):
    if "instruct:buy" in action:
        return 'Buy'
    return 'Sell'


def create(nos: NewOrderSingle):
    repo = model.MarketOrder(hash_key=pk(nos.uuid),
                             range_key=sk(nos.uuid),
                             uuid=nos.uuid,
                             state=nos.state,
                             tags=nos.serialise_tags())
    repo.save()
    return repo

def find_by_id(uuid) -> NewOrderSingle:
    repo = model.NewOrderSingle.get(pk(uuid), sk(uuid))
    return Instruction(uuid=repo.uuid,
                       state=repo.state,
                       instruction=repo.instruction)


def pk(uuid):
    return "MORD#{}".format(uuid)

def sk(uuid):
    return "META#{}".format(uuid)


def unique_id():
    return str(uuid.uuid4())
