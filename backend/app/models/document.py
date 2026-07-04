from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from app.db.mysql import Base

class Document(Base):

    __tablename__ = "documents"

    document_id = Column(
        String(36),
        primary_key=True
    )

    filename = Column(
        String(255),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.user_id")
    )