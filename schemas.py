

from pydantic import BaseModel
from typing import Optional

# User Schemas
class UserBase(BaseModel):
    username: str
    password: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

# Question Schemas
class QuestionBase(BaseModel):
    question_text: str
    correct_answer: str
    difficulty: str

class Question(QuestionBase):
    id: int

    class Config:
        orm_mode = True

# Game Schemas
class GameBase(BaseModel):
    score: float
    difficulty: str
    name: str
    current_question: Optional[int]

class GameCreate(GameBase):
    user_id: int

class Game(GameBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

# Answer submission schema
class SubmitAnswerRequest(BaseModel):
    game_id: int
    question_id: int
    user_answer: str

class SubmitAnswerResponse(BaseModel):
    message: str
    next_question: Optional[Question] = None
    final_score: Optional[float] = None

    class Config:
        orm_mode = True
