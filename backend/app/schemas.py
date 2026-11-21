# APIの出力の型を切り出す

from pydantic import BaseModel

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

class AnswerIn(BaseModel):
    option_id: int

class AnswerOut(BaseModel):
    is_correct: bool
    correct_option_id: int
    que_explanation: str