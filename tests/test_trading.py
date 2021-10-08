from .shared import *

from trading.instructor import handler as instructor

def test_buy_instruction(buy_instruction):
    client_id, instruction_id = instructor.create(buy_instruction)
    instructor.commit(client_id)

    breakpoint()