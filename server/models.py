from sqlalchemy import create_engine, Table, String, Column, Integer, MetaData, DateTime
from sqlalchemy.orm import mapper

engine = create_engine('sqlite:///../chat.db')

metadata = MetaData()

responses = Table(
    'responses', metadata,
    Column('id', Integer, primary_key=True),
    Column('action', String),
    Column('datetime', DateTime),
    Column('data', String),
    Column('code', Integer),
)

metadata.create_all(engine)


class Response:
    def __init__(self, action, datetime, data, code):
        self.action = action
        self.datetime = datetime
        self.data = data
        self.code = code


mapper(Response, responses)

