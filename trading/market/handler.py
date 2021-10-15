from pyfuncify import monad, fn

from .domain import market as domain

def financial_product_decisions(req):
    return monad.Right(req) >> find_listing >> instructable_decision >> assertion_result

def find_listing(req):
    fp, listing = domain.find_listed_instrument(req['financialProduct'])
    return monad.Right(
        {
            'req': req,
            'listing': listing,
            'financial_product': fp,
            'assertions': []
        }
    )

def instructable_decision(value):
    value['assertions'] = fn.remove_none(map(lambda f: f(value), rules()))
    return monad.Right(value)

def rules():
    return [price_sanity_assert, expiry_market_date, price_tick]

def price_sanity_assert(value):
    return domain.price_sanity_assert(value)

def expiry_market_date(value):
    return domain.expiry_market_date(value)

def price_tick(value):
    return domain.price_tick(value)

def assertion_result(value):
    return {
        'assertions': value['assertions'],
        'decision_outcome': domain.decision_outcome(value['assertions']),
        'financial_product_context': domain.financial_product_microformat(value['financial_product'], value['listing'])
    }

