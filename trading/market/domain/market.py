from pymonad.tools import curry
from pyfuncify import fn

from .financial_product import *

nzl_jur = GeographicJurisdiction(handle="urn:trading:jur:NZL", iso3166_country_code="urn:common:iso3166Country:NZL")
aus_jur = GeographicJurisdiction(handle="urn:trading:jur:AUS", iso3166_country_code="urn:common:iso3166Country:AUS")

nzx = Market(name="nzx", iso20222_mic="nzx", iso20222_op_mic="xnzx", trading_jurisdiction=nzl_jur)
asx = Market(name="asx", iso20222_mic="asx", iso20222_op_mic="xasx", trading_jurisdiction=aus_jur)

spk_ven_lstg_nzx = VenueListing(id="id:lst:spk:nzl:nzx", listing_identity='spk.nz', symbol='spk', listed_at=nzx)
spk_ven_lstg_asx = VenueListing(id="id:lst:spk:aus:asx", listing_identity='spk.au', symbol='spk', listed_at=asx)

spk_fp = FinancialProduct(id='id:fp:spk',
                          asset_class='equity',
                          gics_class='gics/a/b/c',
                          cfi_code=["E","S","V","U","F","N"],
                          sedol="",
                          isin="isin:1",
                          permid='permid:1',
                          openfigi_id='openfigi:1',
                          listings=[spk_ven_lstg_nzx, spk_ven_lstg_asx])

financial_products = [spk_fp]

def find_listed_instrument(fp):
    return fn.find(by_fp_id, financial_products).for_listed_jurisdiction(fp['tradingJurisdiction'])

@curry(2)
def by_fp_id(fp_id, fp):
    return fp.id == fp_id

def price_sanity_assert(value):
    outcome, msg = value['listing'].sane_price(value['req']['context']['price'])
    if outcome == "success":
        return None
    return {
      'decision': ["urn:trading:decision:instrument_instructable"],
      'rule': "urn:trading:decisionAssert:priceSanityAssert",
      'value': "urn:trading:decisionAssert:priceSanityAssertion:priceOutSideLimits",
      'outcome': outcome,
      'msg': msg,
      'ctx': {}
    }

def expiry_market_date(value):
    outcome, msg = value['listing'].valid_expiry(value['req']['context']['expiry'])
    if outcome == "success":
        return None
    return {
      'decision': ["urn:trading:decision:instrument_instructable"],
      'rule': "urn:trading:decisionAssert:expiryMarketDate",
      'value': "urn:trading:decisionAssert:expiryMarketDate:expiryOutsideMarketDate",
      'outcome': outcome,
      'msg': msg,
      'ctx': {}
    }

def price_tick(value):
    outcome, msg = value['listing'].valid_price_tick(value['req']['context']['price'])
    if outcome == "success":
        return None
    return {
      'decision': ["urn:trading:decision:instrument_instructable"],
      'rule': "urn:trading:decisionAssert:priceTick",
      'value': "urn:trading:decisionAssert:priceSanityAssertion:underMininumTick",
      'outcome': outcome,
      'msg': "",
      'ctx': {}
    }


def decision_outcome(assertions):
    if all(map(assertion_success, assertions)):
        return 'urn:trading:decisionAssert:assertResult:success'
    return 'urn:trading:decisionAssert:assertResult:reject'

def assertion_success(assertion):
    return assertion['outcome'] == 'success'


def financial_product_microformat(fp, listing) -> dict:
    """
    @context(
      @type(https://schema.jarden.io/contexts/clientFpInstructingStrategy)
     jar-trade(http://jarden.io/ontology/trading)
    )
    strategyContext(trading)
    searchConditions(tr-fin:hasExchangeTicker(CBA))
    financialProduct(id(<uuid>))
    jar-trade:venueStrategy(
      jar-trade:venueExecutionStrategy(urn:trading:venueStrategy:bestExec),
      tradingChannels[
        (
          @id(uuid),
          jurisdictionBroker(id:(uuid)),
          jar-party:handle(oa),
          jar-trade:listings[(id(uuid), jar-trade:opMic(XASX)), (id(uuid), jar-trade:opMic(CHIA))]
        ),
        (
          @id(uuid),
          jurisdictionBroker(id:(uuid)),
          jar-party:handle(jar),
          jar-trade:listings[(id(uuid), jar-trade:opMic(XASX)), (id(uuid), jar-trade:opMic(CHIA))]
        )
      ]
    )
    :param fp:
    :param listing:
    :return: dict
    """
    return {
        "@context": {
            "@type": "https://schema.jarden.io/contexts/clientFpInstructingStrategy",
            "jar-trade": "http://jarden.io/ontology/trading"
        },
        "strategyContext": "trading",
        "financialProduct": {
            "id": fp.id
        },
        'venueStrategy': {
            'tradingChannels': [
                {
                    "@id": "channel.id",
                    "jurisdictionBroker": {},
                    "jar-party:handle": "",
                    "jar-trade:listing": {
                        "@id": listing.id,
                        "jar-trade:opMic": listing.listed_at.iso20222_op_mic
                    }
                }
            ]
        }
    }