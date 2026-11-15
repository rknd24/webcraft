from app.database import SessionLocal
from app.models import Category, Question, Option

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

with SessionLocal() as session:
    category = Category(category_name=CATEGORY_NAME)
    session.add(category)
    session.flush()  # category.category_id が使えるようになる

    for q in QUESTIONS:
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

    session.commit()
