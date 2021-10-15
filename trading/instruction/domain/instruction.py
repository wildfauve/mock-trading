from typing import Optional
from dataclasses import dataclass
from pyfuncify import fn
from pymonad.tools import curry

from ..model import instruction_model as model

from ...trading_client import handler as trading_client_service
from ...market import handler as market_service

@dataclass
class Instruction():
    uuid: str
    instruction: dict
    state: str
    cord_uuid: Optional[str] = None
    repo: Optional[model.Instruction] = None


def create(ins: Instruction):
    repo = model.Instruction(hash_key=pk(ins.uuid),
                             range_key=sk(ins.uuid),
                             uuid=ins.uuid,
                             state=ins.state,
                             instruction=ins.instruction)
    repo.save()
    ins.repo = repo
    return ins

def add_cord_uuid(ins: Instruction, cord_uuid: str) -> Instruction:
    ins.cord_uuid = cord_uuid
    ins.repo.cord_uuid = cord_uuid
    ins.repo.save()
    return ins

def find_by_id(uuid) -> Instruction:
    repo = model.Instruction.get(pk(uuid), sk(uuid))
    return Instruction(uuid=repo.uuid,
                       state=repo.state,
                       instruction=repo.instruction.as_dict(),
                       cord_uuid=repo.cord_uuid,
                       repo=repo)

def state_transition_ins_to_in_submittment(ins):
    ins.state = 'in_submittment'
    ins.repo.state = ins.state
    ins.repo.save()
    return ins

def trading_client_assertions(ins):
    return trading_client_service.trading_client_decisions(tc_assertion_req(trading_client_ctx(ins)))


def financial_product_assertions(ins):
    return market_service.financial_product_decisions(fp_assertion_req(ins['financialProduct'], fp_ctx(ins)))


def tc_assertion_req(tc_ctx):
    return {
        "tradingClient": {"id":  tc_ctx['trading_client']['id']},
        "context": {
            "tradingJurisdiction": tc_ctx['trading_jurisdiction'],
            "contract": {"id": tc_ctx['contract']['id']}
            },
        "decisions": ["urn:client:decision:tradeable", "urn:client:decision:settleable"]
    }

def fp_assertion_req(fp, fp_ctx):
    return {
        "financialProduct": fp,
        "context": fp_ctx,
        "decisions": ["urn:trading:decision:instrumentInstructable"]
    }

def trading_client_ctx(ins):
    return {
        'trading_client': ins['instructingParties']['tradingParty'],
        'contract': ins['contract'],
        'trading_jurisdiction': instructing_trading_jurisdiction(ins['financialProduct'])
    }

def fp_ctx(ins):
    return {
        "action": ins['action'],
        "price": ins['strategy']['price'],
        "venueStrategy": ins['strategy']['channelStrategy'],
        "expiry": ins['strategy']['inForceStrategy']['expiry'],
        "inForce": ins['strategy']['inForceStrategy']['inForce']
    }

def instructing_trading_jurisdiction(fp):
    return fp['tradingJurisdiction']

def pk(uuid):
    return "CINS#{}".format(uuid)

def sk(uuid):
    return "META#{}".format(uuid)
