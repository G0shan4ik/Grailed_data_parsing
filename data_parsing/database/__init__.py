from peewee import (
    TextField,
    Model,
    IntegerField,
    SqliteDatabase,
)

from pathlib import Path
from os import getcwd


path = Path(getcwd()).joinpath('grailed_ph.db')
db = SqliteDatabase(path)
print(path)


class BaseModel(Model):
    class Meta:
        database = db


class CardData(BaseModel):
    id = IntegerField(null=False, primary_key=True)
    designer = TextField(null=False)
    name = TextField(null=False)
    size = TextField(null=False)
    color = TextField(null=False)
    condition = TextField(null=False)
    sold_price = IntegerField(null=False)
    authenticated = TextField(null=False, default='false')
    seller = TextField(null=False)
    seller_url   = TextField(null=False)
    description = TextField(null=False)
    listed_at = TextField(null=False)
    favorites = IntegerField(null=False)
    url = IntegerField(null=False)
    gender = TextField(null=False)
    category = TextField(null=False)
    subcategory = TextField(null=False)
    sold_at = TextField(null=False)
    photo_url = TextField(null=False)


def init():
    CardData.create_table(safe=True)