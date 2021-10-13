from pyfuncify import monad
import uuid

from .domain import instruction as domain
from ..broker import handler as broker_service


def offer(instruction):
    return monad.Right(instruction) >> assign_id >> offer_instruction >> offer_result


def commit(ins_id):
    return monad.Right(ins_id) >> find >> instruction_submitted_event >> update_ins_to_in_submittment

def get_ins_by_uuid(ins_id):
    return domain.find_by_id(ins_id)

def assign_id(instruction):
    instruction['uuid'] = unique_id()
    return monad.Right(instruction)


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
