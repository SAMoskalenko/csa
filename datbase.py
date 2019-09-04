from sqlalchemy import create_engine, Table, String, Column, Integer, MetaData
from sqlalchemy.orm import mapper

engine = create_engine('sqlite:///chat.db')

metadata = MetaData()

metadata.create_all(engine)