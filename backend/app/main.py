from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import select
from app.models import Category, Question, Option
from sqlalchemy.orm import Session
from app.database import get_db


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


@app.get("/categories",response_model=list[CategoryOut])
def get_categories(db: Session=Depends(get_db)):
    categories = db.scalars(select(Category)).all()
    if not categories:
        raise HTTPException(status_code=500, detail="カテゴリが登録されていません")
    return [{"category_id": category.category_id, "category_name": category.category_name} for category in categories]


@app.get("/questions/{que_id}", response_model=QuestionOut)
def get_question(que_id: int, db: Session = Depends(get_db)):
    q = db.scalars(select(Question).where(Question.que_id == que_id, Question.is_deleted == False)).first()
    if q is None:
        raise HTTPException(status_code=404, detail="問題が見つかりませんでした" )
    options = db.scalars(select(Option).where(Option.que_id == que_id)).all()
    if not options:
        raise HTTPException(status_code=500, detail="データの不備" )
    return {
        "que_id": q.que_id,
        "que_statement": q.que_statement,
        "options": [{"option_id": option.option_id, "option_text": option.option_text} for option in options ]
    }



