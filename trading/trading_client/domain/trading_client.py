from typing import Tuple
from pymonad.tools import curry

from pyfuncify import fn

tc1 = {
    'id': 'trading_client_1',
    'contractId': 'client_1_contract_direct',
    'tradingCounterparties': [
        {
            'id': '034de9a0-8d94-403a-8f87-f046fcdfbf30',
            'provider': {
                'designation': 'urn:client:counterparty:provider:jardenNewZealand',
            },
            'counterpartyAccountId': 'some-counterpartyCode-2',
            'identifiers': [
                {'type': 'urn:securitEase:cpCode', 'value': 'some-counterpartyCode-2'},
                {'type': 'urn:securitEase:cpAccountId', 'value': 'some-accountId-3'},
            ],
            'jurisdictions': ['urn:common:iso3166Country:NZL','urn:common:iso3166Country:AUS'],
            'state': 'urn:client:counterparty:state:onboarding',
            'created': {'date': '2021-10-13T02:37:27.054Z', 'microseconds': 0.054},
            'updated': {'date': '2021-10-13T02:37:27.054Z', 'microseconds': 0.054}
        }
    ],
    'settlementVenues': [
        {
            'id': '7617d1f6-a2ed-422a-9f6a-d4c549cbe89e',
            'provider': {
                'designation': 'urn:client:counterparty:provider:jardenNewZealand'
            },
            'providerIdentifiers': [
                {'type': 'urn:securitEase:cpCode', 'value': 'some-counterpartyCode-2'},
                {'type': 'urn:securitEase:cpAccountId', 'value': 'some-accountId-3'}
            ],
            'jurisdiction': 'urn:common:iso3166Country:NZL',
            'settlementModes': [
                {
                    'mode': 'OWN_NAME',
                    'modeQualifier': 'CSN',
                    'identifiers': [{'type': 'CSN', 'value': 'some-shareholderNumber-6'}],
                    'method': 'DVP'
                }
            ],
            'created': '2021-10-13T02:37:27.054Z',
            'updated': '2021-10-13T02:37:27.054Z'
        }
    ],
    'created': '2021-10-13T02:37:27.027Z',
    'updated': '2021-10-13T02:37:27.027Z'
}

tcs = {'trading_client_1': tc1}

def find_by_id(uuid):
    return tcs[uuid]

def trading_assertions(value) -> Tuple[dict, dict]:
    outcome, onboarding_rule, onboarding_rule_value, ctx = onboarding_rule_assertion(value['req']['context'],
                                                                                value['trading_client'])
    return (
        ctx,
        {
          'decision': ["urn:client:decision:tradeable"],
          'rule': onboarding_rule,
          'value': onboarding_rule_value,
          'outcome': outcome,
          'msg': "",
          'ctx': {}
        }
    )
def onboarding_rule_assertion(ctx, tc):
    cp_for_jur = fn.find(trading_cp_for_jurisdiction(ctx['tradingJurisdiction']), tc['tradingCounterparties'])
    if cp_for_jur is None:
        return ('failure',
                "urn:client:decisionAssert:counterPartyProviderAssert",
                "urn:client:decisionAssert:counterPartyProviderAssert:tradingInJurisdictionUnavailable",
                None)

    return ('success',
            "urn:client:decisionAssert:counterPartyProviderAssert",
            "urn:client:decisionAssert:counterPartyProviderAssert:active",
            cp_for_jur)

def settling_assertions(value) -> Tuple[dict, dict]:
    outcome, settle_rule, settle_rule_value, ctx = settling_rule_assertion(value['req']['context'],
                                                                           value['trading_client'])
    return (
        ctx,
        {
          'decision': ["urn:client:decision:tradeable"],
          'rule': settle_rule,
          'value': settle_rule_value,
          'outcome': outcome,
          'msg': "",
          'ctx': {}
        }
    )

def settling_rule_assertion(ctx, tc):
    sv_for_jur = fn.find(settlement_venue_for_jurisdiction(ctx['tradingJurisdiction']), tc['settlementVenues'])
    if sv_for_jur is None:
        return ('failure',
                "urn:client:decisionAssert:settlementVenueAssert",
                "urn:client:decisionAssert:settlementVenueAssert:settlementVenueUnavailable",
                None)

    return ('success',
            "urn:client:decisionAssert:settlementVenueAssert",
            "urn:client:decisionAssert:settlementVenueAssert:active",
            sv_for_jur)

def decision_outcome(assertions):
    if all(map(assertion_success, assertions)):
        return 'urn:client:decisionAssert:assertResult:success'
    return 'urn:client:decisionAssert:assertResult:reject'

@curry(2)
def trading_cp_for_jurisdiction(jur, cp):
    return jur in cp['jurisdictions']

@curry(2)
def settlement_venue_for_jurisdiction(jur, venue):
    return jur == venue['jurisdiction']

def assertion_success(assertion):
    return assertion['outcome'] == 'success'