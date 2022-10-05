import os
from datetime import datetime

from peewee import *

db = MySQLDatabase(
    os.getenv('DATABASE_NAME'),
    user=os.getenv('DATABASE_USER'),  # Will be passed directly to psycopg2.
    password=os.getenv('DATABASE_PASSWORD'),
    host=os.getenv('DATABASE_HOST'), )


class BaseModel(Model):
    class Meta:
        database = db


class Game(BaseModel):
    guid_user = UUIDField(null=False, index=True)
    created_date = DateTimeField(default=datetime.now)


class ListNumber(BaseModel):
    game = ForeignKeyField(Game)
    number_chosen = IntegerField(null=False)
    created_date = DateTimeField(default=datetime.now)
