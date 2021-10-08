import uuid

from . import state
from ..instruction import handler as instruction_service

def create(instruction):
    client_id = generate_client_id()
    add_to_state(client_id, instruction)
    _ok, ins_id = offer_instruction(client_id)
    update_ins_with_id(client_id, ins_id)
    return (client_id, ins_id)

def commit(client_id):
    ins_id, ins = get_instruction_from_state(client_id)
    instruction_service.commit(ins_id)
    breakpoint()
    pass

def add_to_state(client_id, instruction):
    instruction['clientId'] = client_id
    ins_state = state.Instructions().add_instruction(client_id, None, instruction)
    return ins_state

def update_ins_with_id(client_id, ins_id):
    state.Instructions().add_id(client_id, ins_id)
    pass

def offer_instruction(client_id):
    ins_id, ins = get_instruction_from_state(client_id)
    return instruction_service.offer(ins)


def generate_client_id():
    return str(uuid.uuid4())


def get_instruction_from_state(ins_id):
    return state.Instructions().get_instruction_by_id(ins_id)