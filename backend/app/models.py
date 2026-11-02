from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy import String
from sqlalchemy import Identity
from sqlalchemy import ForeignKey
from sqlalchemy import Text
from sqlalchemy import text
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import MetaData
from datetime import datetime

class Base(DeclarativeBase):
    # 制約の名前を決める規則。PostgreSQLが自動で付ける名前（テーブル名_列名_fkey、テーブル名_pkey）に合わせている。
    metadata = MetaData(naming_convention={
        "fk": "%(table_name)s_%(column_0_name)s_fkey",
        "pk": "%(table_name)s_pkey",
    })

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
    category_id: Mapped[int] = mapped_column( ForeignKey("category.category_id", ondelete="RESTRICT"))
    que_statement: Mapped[str] = mapped_column(Text)
    que_explanation: Mapped[str] = mapped_column(Text)
    is_deleted: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))

class Option(Base):
    __tablename__ = "option"

    option_id: Mapped[int] = mapped_column( Identity(start=1, always=True), primary_key=True)
    que_id: Mapped[int] = mapped_column( ForeignKey("question.que_id", ondelete="CASCADE"))
    option_text: Mapped[str] = mapped_column(Text)
    is_correct: Mapped[bool] = mapped_column(Boolean)

class WeakPoint(Base):
    __tablename__ = "weak_point"

    user_id: Mapped[int] = mapped_column( ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    que_id: Mapped[int] = mapped_column( ForeignKey("question.que_id", ondelete="RESTRICT"), primary_key=True)

class AnsHistory(Base):
    __tablename__ = "ans_history"

    ans_id: Mapped[int] = mapped_column( Identity(start=1, always=True), primary_key=True)
    user_id: Mapped[int] = mapped_column( ForeignKey("users.user_id", ondelete="CASCADE"))
    selected_option_id: Mapped[int] = mapped_column( ForeignKey("option.option_id", ondelete="RESTRICT"))
    time_stamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    