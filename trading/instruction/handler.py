from pyfuncify import monad
import uuid

from .domain.instruction import Instruction, Instructions
from ..broker import handler as broker_service


def offer(instruction):
    return monad.Right(instruction) >> assign_id >> offer_instruction >> create_result


def commit(ins_id):
    return monad.Right(ins_id) >> find >> instruction_submitted_event

def assign_id(instruction):
    instruction['uuid'] = unique_id()
    return monad.Right(instruction)


def offer_instruction(instruction):
    ins = Instruction(uuid=instruction['uuid'], instruction=instruction, state='created')
    Instructions().add(ins)
    return monad.Right(ins)


def create_result(instruction):
    return ('ok', instruction.uuid)


def find(ins_id) -> Instruction:
    return monad.Right(Instructions().find_by_id(ins_id))

def instruction_submitted_event(ins):
    broker_service.submitted_event(ins)
    return monad.Right('ok')


def unique_id():
    return str(uuid.uuid4())
