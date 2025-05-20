from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import declarative_base
from pgvector.sqlalchemy import Vector

from app.core.config import settings

Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(String, index=True, nullable=False)
    user_id = Column(String, index=True, nullable=True)  # Nullable as per spec
    role = Column(String, nullable=False)  # e.g., "user", "model"
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    embedding = Column(Vector(settings.EMBEDDING_DIMENSION))

    def __repr__(self):
        return f"<Message(id={self.id}, session_id='{self.session_id}', role='{self.role}')>" 