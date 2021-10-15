from .shared import *

from trading.instructor import handler as instructor

def test_buy_instruction(dynamo_setup, buy_instruction):
    client_id, instruction_id = instructor.create(buy_instruction)

    instructor.commit(client_id)

    inst = instructor.get_instruction_by_client_id(client_id)

    assert inst.state == 'in_submittment'
    breakpoint()