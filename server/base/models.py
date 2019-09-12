from datetime import datetime
from sqlalchemy import String, Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from server.auth.models import User

from server.database import Base


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    action = Column(String, nullable=True)
    data = Column(String, nullable=True)
    created = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='messages')

    @property
    def is_anonimous(self):
        return self.user is None
