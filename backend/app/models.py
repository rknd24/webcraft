from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy import String
from sqlalchemy import Identity
from sqlalchemy import ForeignKey
from sqlalchemy import Text
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column( Identity(start=1, always=True), primary_key=True)
    user_name: Mapped[str] = mapped_column(String(50))

class Category(Base):
    __tablename__ = "category"

    category_id: Mapped[int] = mapped_column( Identity(start=1, always=True), primary_key=True)
    category_name: Mapped[str] = mapped_column(String(50))

class Question(Base):
    __tablename__ = "question"

    que_id: Mapped[int] = mapped_column( Identity(start=1, always=True), primary_key=True)
    category_id: Mapped[int] = mapped_column( ForeignKey("category.category_id"))
    que_statement: Mapped[str] = mapped_column(Text)
    que_explanation: Mapped[str] = mapped_column(Text)

class Option(Base):
    __tablename__ = "option"

    option_id: Mapped[int] = mapped_column( Identity(start=1, always=True), primary_key=True)
    que_id: Mapped[int] = mapped_column( ForeignKey("question.que_id"))
    option_text: Mapped[str] = mapped_column(Text)
    is_correct: Mapped[bool] = mapped_column(Boolean)

class WeakPoint(Base):
    __tablename__ = "weak_point"

    user_id: Mapped[int] = mapped_column( ForeignKey("users.user_id"), primary_key=True)
    que_id: Mapped[int] = mapped_column( ForeignKey("question.que_id"), primary_key=True)

class AnsHistory(Base):
    __tablename__ = "ans_history"

    ans_id: Mapped[int] = mapped_column( Identity(start=1, always=True), primary_key=True)
    user_id: Mapped[int] = mapped_column( ForeignKey("users.user_id"))
    selected_option_id: Mapped[int] = mapped_column( ForeignKey("option.option_id"))
    time_stamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    