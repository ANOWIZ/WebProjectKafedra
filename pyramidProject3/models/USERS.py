from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
)

from .meta import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    password = Column(Text)

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def __repr__(self):
        return "<User('%s','%s')>" % (self.name, self.password)