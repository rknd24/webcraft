from sqlalchemy import select

from app.database import SessionLocal
from app.models import Category, Option, Question
from app.rules import validate_choices

# 動作確認用のデータ。問題を増やすときは、QUESTIONS に1つ足す。
CATEGORY_NAME = "HTTP通信"

QUESTIONS = [
    {
        "statement": "何か情報をとってくる際のHTTPメソッド名はどれか",
        "explanation": "Getメソッドです",
        "choices": [("Get", True), ("Post", False), ("Put", False), ("Patch", False)],
    },
    {
        "statement": "リソースが見つからないときに返るHTTPステータスコードはどれか",
        "explanation": "404 Not Found です",
        "choices": [("200", False), ("301", False), ("404", True), ("500", False)],
    },
]


def get_or_create_category(session, name):
    """同じ名前のカテゴリがあれば、それを使う。なければ作る（何度実行しても、重複しない）。"""
    category = session.scalars(
        select(Category).where(Category.category_name == name).order_by(Category.category_id)
    ).first()
    if category is None:
        category = Category(category_name=name)
        session.add(category)
        session.flush()  # category.category_id が使えるようになる
    return category


def seed(session):
    """データを入れる。戻り値は（追加した問題の数, すでにあったので飛ばした問題の数）。"""
    # 入れる前に、全部の問題を検査する（1問でもおかしければ、何も入れない）
    for q in QUESTIONS:
        validate_choices([is_correct for _, is_correct in q["choices"]])

    category = get_or_create_category(session, CATEGORY_NAME)
    added = skipped = 0
    for q in QUESTIONS:
        # 同じ問題文の問題が、すでにあれば、飛ばす
        exists = session.scalars(
            select(Question).where(Question.que_statement == q["statement"])
        ).first()
        if exists is not None:
            skipped += 1
            continue

        question = Question(
            category_id=category.category_id,
            que_statement=q["statement"],
            que_explanation=q["explanation"],
        )
        session.add(question)
        session.flush()  # question.que_id が使えるようになる
        session.add_all(
            [
                Option(que_id=question.que_id, option_text=text, is_correct=is_correct)
                for text, is_correct in q["choices"]
            ]
        )
        added += 1
    return added, skipped


if __name__ == "__main__":
    with SessionLocal() as session:
        added, skipped = seed(session)
        session.commit()
    print(f"追加した問題：{added} 問 / すでにあったので飛ばした問題：{skipped} 問")
