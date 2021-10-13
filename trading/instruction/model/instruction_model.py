from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute, MapAttribute, ListAttribute,DiscriminatorAttribute
)


class BaseModel(Model):
    """
    Base Model consisting of the single table convention; the hash and range keys named PK and SK respectively.
    """
    class Meta:#(Model.Meta):
        table_name = "instruction"
        host = "http://localhost:8000"
        write_capacity_units = 1
        read_capacity_units = 1
    PK = UnicodeAttribute(hash_key=True)
    SK = UnicodeAttribute(range_key=True)
    kind = DiscriminatorAttribute()


class Instruction(BaseModel, discriminator='instruction'):
    cord_uuid = UnicodeAttribute(null=True)
    instruction = MapAttribute()
    uuid = UnicodeAttribute()
    state = UnicodeAttribute()


def delete_table():
    BaseModel.delete_table()
    ...

def create_table():
    if not BaseModel.exists():
        BaseModel.create_table()
    ...
