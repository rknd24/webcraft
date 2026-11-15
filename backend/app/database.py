import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# .env の DATABASE_URL を読む（Alembic の env.py と同じ読み方）
load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]

# engine：DBにつなぐ元。アプリで1つだけ作る。作った時点ではまだDBにつながらない。
engine = create_engine(DATABASE_URL)

# SessionLocal：Session（DBとの1回のやり取りの単位）を作る工場。engine と同じ範囲で、1回だけ作る。
SessionLocal = sessionmaker(engine)


def get_db():
    """リクエストごとに新しい Session を渡し、終わったら必ず閉じる（FastAPIの yield を使う依存関係）。"""
    with SessionLocal() as db:
        yield db
