from app.models import Category, Option, Question

TEST_CATEGORY_NAME = "テスト用カテゴリ"

TEST_QUESTION = {
    "statement": "テスト用の問題",
    "explanation": "テスト用の解説",
    "choices": [("正解", True), ("不正解1", False), ("不正解2", False), ("不正解3", False)]
}

def test_is_correct(client, db_session):
    category = Category(category_name=TEST_CATEGORY_NAME)
    db_session.add(category)
    db_session.flush()
    question = Question(
        category_id = category.category_id,
        que_statement = TEST_QUESTION["statement"],
        que_explanation = TEST_QUESTION["explanation"],
    )
    db_session.add(question)
    db_session.flush()
    options = [
                Option(que_id=question.que_id, option_text=text, is_correct=is_correct)
                for text, is_correct in TEST_QUESTION["choices"]
    ]
    db_session.add_all(options)
    db_session.flush()
    correct = [option for option in options if option.is_correct][0]
    res = client.post(f"/questions/{question.que_id}/answers", json = {"option_id": correct.option_id})
    assert res.status_code == 200
    assert res.json()["is_correct"] == True
    assert res.json()["correct_option_id"] == correct.option_id
