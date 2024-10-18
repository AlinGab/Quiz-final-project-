from pydantic import BaseModel
from typing import List, Dict


class UserBase(BaseModel):
    name: str
    username: str
    password: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True


#Model de joc
class GameBase(BaseModel):
    score: int
    current_question_id: int
    user_id: int
    class Config:
        orm_mode = True

class GameCreate(GameBase):
    pass

class Game(GameBase):
    id: int
    class Config:
        orm_mode = True

class QuestionBase(BaseModel):
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str
    difficulty: str

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int

    class Config:
        orm_mode = True






