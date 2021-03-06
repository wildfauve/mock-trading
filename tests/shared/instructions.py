import pytest

@pytest.fixture
def buy_instruction():
    return {
        'action': 'urn:trading:action:instruct:buy',
        'clientId': None,
        'instructingParties': {
            'tradingParty': {
                'type': 'urn:identity:tradingClient',
                'id': 'trading_client_1',
                'name': '<str>'
            },
            'responsibleParty': {
                'type': 'urn:identity:party',
                'id': '<uuid>',
                'name': '<str>'
            },
            'instructingSubject': {
                'type': 'urn:identity:profile',
                'id': '<uuid>',
                'name': '<str>'
            }
        },
        'contract': {
            'id': 'client_1_contract_direct',
            'businessUnit': 'DIRECT'
        },
        'financialProduct': {
            'id': 'id:fp:spk',
            'tradingJurisdiction': 'urn:common:iso3166Country:NZL'
        },
        'strategy': {
            'execution': 'urn:trading:executionStrategy:limit',
            'qty': {
              'type': '??',
              'unitCode': 'unit',
              'value': 100
            },
            'priceStrategy': 'urn:trading:priceStrategy:atUnit',
             'price': {
              'price': '10.10',
              'priceCurrency': 'AUD'
            },
            'inForceStrategy': {
              'inForce': 'urn:trading:inForceStrategy:goodTillDate',
              'expiry': '{{iso8601-time-utc}}'
            },
            'channelStrategy': 'urn:trading:venueStrategy:bestExec'
        }
    }