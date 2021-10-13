from typing import Optional
from dataclasses import dataclass
from pyfuncify import fn
from pymonad.tools import curry

from ..model import instruction_model as model

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

def pk(uuid):
    return "CINS#{}".format(uuid)

def sk(uuid):
    return "META#{}".format(uuid)
