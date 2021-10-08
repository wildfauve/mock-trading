class Instructions():
    state = {}

    def add_instruction(self, client_id, ins_id, instruction):
        self.state[client_id] = (ins_id, instruction)
        return self

    def add_id(self, client_id, ins_id):
        existing_ins_id, inst = self.get_instruction_by_id(client_id)
        self.add_instruction(client_id, ins_id, inst)
        pass

    def get_instruction_by_id(self, client_id):
        return self.state[client_id]
