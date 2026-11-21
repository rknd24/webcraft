from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import select, func
from app.models import Category, Question, Option
from sqlalchemy.orm import Session
from app.database import get_db
from app.rules import validate_choices


app = FastAPI()

class CategoryOut(BaseModel):
    category_id: int
    category_name: str

class OptionOut(BaseModel):
    option_id: int
    option_text: str

class QuestionOut(BaseModel):
    que_id: int
    que_statement: str
    options: list[OptionOut]

def load_question_with_options(db, que_id):
    q = db.scalars(select(Question).where(Question.que_id == que_id, Question.is_deleted == False)).first()
    if q is None:
        return None
    options = db.scalars(select(Option).where(Option.que_id == que_id)).all()
    validate_choices([option.is_correct for option in options])
    return q, options


@app.get("/categories",response_model=list[CategoryOut])
def get_categories(db: Session=Depends(get_db)):
    categories = db.scalars(select(Category)).all()
    if not categories:
        raise HTTPException(status_code=500, detail="カテゴリが登録されていません")
    return [{"category_id": category.category_id, "category_name": category.category_name} for category in categories]


@app.get("/questions/random",response_model=QuestionOut)
def get_random_question(category_id: int, db: Session= Depends(get_db)):
    q = db.scalars(select(Question).where(Question.category_id == category_id, Question.is_deleted == False).order_by(func.random()).limit(1)).first()
    if q is None:
        raise HTTPException(status_code=404, detail="問題が見つかりません")
    try:
        result = load_question_with_options(db, q.que_id)
    except ValueError:
        raise HTTPException(status_code=500, detail="データの不備")
    if result is None:
        raise HTTPException(status_code=404, detail="問題が見つかりません")
    q, options = result
    return {
        "que_id": q.que_id,
        "que_statement": q.que_statement,
        "options": [{"option_id": option.option_id, "option_text": option.option_text} for option in options]
    }



@app.get("/questions/{que_id}", response_model=QuestionOut)
def get_question(que_id: int, db: Session = Depends(get_db)):
    try:
        result = load_question_with_options(db, que_id)
    except ValueError:
        raise HTTPException(status_code=500, detail="データの不備")
    if result is None:
        raise HTTPException(status_code=404, detail="問題が見つかりません")
    q, options = result
    return {
        "que_id": q.que_id,
        "que_statement": q.que_statement,
        "options": [{"option_id": option.option_id, "option_text": option.option_text} for option in options ]
    }



