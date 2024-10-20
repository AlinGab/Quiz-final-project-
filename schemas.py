from pydantic import BaseModel
from typing import List, Optional, Literal, Tuple

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
        from_attributes = True

# Model User
class UserBase(BaseModel):
    username: str
    password: str
    name: Optional[str] = None  # Optional for name

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

# Model de joc
class GameBase(BaseModel):
    score: float  # Changed to float for consistency
    current_question: Optional[int] = None  # Optional for current question
    difficulty: str
    user_id: int
    name: str  # Player's name

class GameCreate(GameBase):
    name: str

class Game(GameBase):
    id: int

    class Config:
        from_attributes = True

# Model de răspuns
class Answer(BaseModel):
    question_id: int
    user_id: int
    selected_option: str

    class Config:
        from_attributes = True

# Model pentru scorul utilizatorului (optional, if needed)
class UserScore(BaseModel):
    user_id: int
    score: float

    class Config:
        from_attributes = True

class SubmitAnswer(BaseModel):
    question_id: int
    user_answer: str

class SubmitAnswerRequest(BaseModel):
    game_id: int
    answers: List[SubmitAnswer]

    class Config:
        schema_extra = {
            "example": {
                "game_id": 1,
                "answers": [
                    {"question_id": 1, "user_answer": "A"},
                    {"question_id": 2, "user_answer": "B"},
                    {"question_id": 3, "user_answer": "C"},
                    {"question_id": 4, "user_answer": "D"},
                    {"question_id": 5, "user_answer": "A"}
                ]
            }
        }

class SubmitAnswerResponse(BaseModel):
    message: str
    final_score: Optional[float] = None