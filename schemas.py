from pydantic import BaseModel
from typing import List, Optional

# Schema pentru întrebare
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

#Model user
class UserBase(BaseModel):
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

class GameCreate(GameBase):
    pass

class Game(GameBase):
    id: int

    class Config:
        orm_mode = True

#Model de raspuns
class Answer(BaseModel):
    question_id: int
    user_id: int
    selected_option: str

    class Config:
        orm_mode = True
