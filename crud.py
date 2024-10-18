
from sqlalchemy.orm import Session
from . import models, schemas
import bcrypt

# User Operations
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_name(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# Game Operations
def get_game_by_id_and_user(db: Session, game_id: int, user_id: int):
    return db.query(models.Game).filter(
        models.Game.id == game_id,
        models.Game.user_id == user_id
    ).first()

def update_game_score(db: Session, game: models.Game, increment: float):
    game.score += increment
    db.commit()
    db.refresh(game)
    return game

def validate_answer(db: Session, question_id: int, user_answer: str):
    question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if question:
        if question.correct_answer.lower() == user_answer.lower():
            return 1  # Correct answer
        else:
            return 0  # Incorrect answer
    else:
        raise ValueError("Question not found")

def get_remaining_questions_by_difficulty(db: Session, difficulty: str, answered_question_ids: list):
    return db.query(models.Question).filter(
        models.Question.difficulty == difficulty,
        models.Question.id.notin_(answered_question_ids)
    ).all()

def update_game_current_question(db: Session, game: models.Game, next_question_id: int):
    game.current_question = next_question_id
    db.commit()
    db.refresh(game)
    return game
