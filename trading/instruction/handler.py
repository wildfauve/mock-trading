from pyfuncify import monad
import uuid

from .domain import instruction as domain
from ..broker import handler as broker_service
from ..market import handler as market_service


def offer(instruction):
    return monad.Right(instruction) >> \
           build_instruction >> \
           offer_instruction >> \
           offer_result


def commit(ins_id):
    return monad.Right(ins_id) >> find >> instruction_submitted_event >> update_ins_to_in_submittment

def get_ins_by_uuid(ins_id):
    return domain.find_by_id(ins_id)

def build_instruction(ins):
    ins['uuid'] = unique_id()

    fp = domain.financial_product_assertions(ins)
    if fp['decision_outcome'] != 'urn:trading:decisionAssert:assertResult:success':
        return monad.Left(ins)

    ins['financialProductContext'] = fp['financial_product_context']

    tc = domain.trading_client_assertions(ins)
    if tc['decision_outcome'] != 'urn:client:decisionAssert:assertResult:success':
        return monad.Left(ins)

    ins['tradingClientContext'] = {'counterParty': tc['counter_party'], 'settlementVenue': tc['settlement_venue']}
    return monad.Right(ins)


def offer_instruction(instruction):
    ins = domain.Instruction(uuid=instruction['uuid'], instruction=instruction, state='created')
    domain.create(ins)
    return monad.Right(ins)


def offer_result(instruction):
    return ('ok', instruction.uuid)


def find(ins_id) -> domain.Instruction:
    return monad.Right(domain.find_by_id(ins_id))

def instruction_submitted_event(ins):
    result, cord_uuid = broker_service.event_instruction_submitted(ins)
    domain.add_cord_uuid(ins, cord_uuid)
    return monad.Right(ins)

def update_ins_to_in_submittment(ins):
    domain.state_transition_ins_to_in_submittment(ins)
    return monad.Right(ins)


def unique_id():
    return str(uuid.uuid4())
