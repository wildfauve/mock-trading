from pyfuncify import monad

from .domain import trading_client as domain

def trading_client_decisions(req):
    return monad.Right(req) >> find_tc >> tradable_decision >> settleable_decision >> assertion_result

def find_tc(req):
    return monad.Right(
        {
            'req': req,
            'trading_client': domain.find_by_id(req['tradingClient']['id']),
            'assertions': []
        }
    )

def tradable_decision(value):
    if not tradable_requested(value['req']):
        return value
    provider_ctx, decision = domain.trading_assertions(value)
    value['assertions'].append(decision)
    value['counter_party_provider'] = provider_ctx
    return monad.Right(value)

def settleable_decision(value):
    if not settleable_requested(value['req']):
        return value
    settlement_ctx, decision = domain.settling_assertions(value)
    value['assertions'].append(decision)
    value['settlement_venue'] = settlement_ctx
    return monad.Right(value)


def assertion_result(value):
    return {
        'assertions': value['assertions'],
        'decision_outcome': domain.decision_outcome(value['assertions']),
        'counter_party': value['counter_party_provider'],
        'settlement_venue': value['settlement_venue']
    }

def tradable_requested(req):
    return 'urn:client:decision:tradeable' in req['decisions']

def settleable_requested(req):
    return 'urn:client:decision:settleable' in req['decisions']
