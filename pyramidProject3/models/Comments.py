from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
)

from .meta import Base

class Comments(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    id_user = Column(Text)
    text = Column(Text)

    def __init__(self, id_user, text):
        self.id_user = id_user
        self.text = text