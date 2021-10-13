from typing import List
from functools import reduce

class Tag:

    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.tag = self.name_to_tag(name)
        pass
    
    def name_to_tag(self, name):
        return self.tag_dictionary()[name]

    @staticmethod
    def tag_dictionary():
        return {
            'SecurityID': '48',
            'SecurityIDSource': '22',
            'Account': '1',
            'OrdType': '40',
            'Price': '44',
            'Side': '54',
            'TimeInForce': '59',
            'ExpiryDate': '432',
            'ClOrdID': '11',
            'OrderQty': '38',
            'TransactTime': '60',
            'NoPartyIDs': '543',
            'PartyID': '448',
            'PartyIDSource': '447',
            'PartyRole': '452'
        }
    
class NewOrderSingle():

    def __init__(self, uuid: str, state: str, tags: List[Tag]):
        self.tags = tags
        self.uuid = uuid
        self.state = state
        pass

    def serialise_tags(self):
        return reduce(self.tag_accum, self.tags, {})

    def tag_accum(self, acc: dict, tag: Tag) -> dict:
        acc[tag.tag] = tag.value
        return acc

