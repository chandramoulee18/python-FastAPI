
from .database import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "Posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey(
        "Users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")


class User(Base):

    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    phone_number = Column(String, nullable=False)


class Vote(Base):
    __tablename__ = "Votes"
    user_id = Column(Integer, ForeignKey(
        "Users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey(
        "Posts.id", ondelete="CASCADE"), primary_key=True)
