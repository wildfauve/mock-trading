from dataclasses import dataclass
from pyfuncify import fn
from pymonad.tools import curry


@dataclass
class Instruction():
    uuid: str
    instruction: dict
    state: str


class Instructions():
    instructions = {}

    def add(self, ins: Instruction):
        self.instructions[ins.uuid] = ins
        pass

    def find_by_id(self, ins_id):
        return self.instructions[ins_id]
        # return fn.find(self.uuid_predicate(ins_id), self.instructions)

    @curry(3)
    def uuid_predicate(self, uuid, x):
        return x.uuid == uuid