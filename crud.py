from sqlalchemy.orm import Session
import models
import schemas
import bcrypt




# User Operations

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db_user = models.User(username=user.username, password=hashed_password, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username(db: Session, username: str):
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



def update_game_current_question(db: Session, game: models.Game, next_question_id: int):
    game.current_question = next_question_id
    db.commit()
    db.refresh(game)
    return game

def update_game_with_answers(db: Session, game_id: int, question_ids: list, answers: list, correctness: list):
    game = db.query(models.Game).filter(models.Game.id == game_id).first()

    if game:
        # Add questions and answers
        game.question_1 = question_ids[0]
        game.answer_1 = answers[0]
        game.is_correct_1 = correctness[0]

        game.question_2 = question_ids[1]
        game.answer_2 = answers[1]
        game.is_correct_2 = correctness[1]

        game.question_3 = question_ids[2]
        game.answer_3 = answers[2]
        game.is_correct_3 = correctness[2]

        game.question_4 = question_ids[3]
        game.answer_4 = answers[3]
        game.is_correct_4 = correctness[3]

        game.question_5 = question_ids[4]
        game.answer_5 = answers[4]
        game.is_correct_5 = correctness[4]

        db.commit()
        db.refresh(game)

    return game

# Answer Validation
def validate_answer(db: Session, question_id: int, user_answer: str):
    question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if question:
        if question.correct_answer.lower() == user_answer.lower():
            return 1  # Correct answer
        else:
            return 0  # Incorrect answer
    else:
        raise ValueError("Question not found")


# Remaining Questions
def get_remaining_questions_by_difficulty(db: Session, difficulty: str, answered_question_ids: list):
    return db.query(models.Question).filter(
        models.Question.difficulty == difficulty,
        models.Question.id.notin_(answered_question_ids)
    ).all()


def get_questions_by_difficulty(db: Session, difficulty: str):
    return db.query(models.Question).filter(models.Question.difficulty == difficulty).all()


def validate_answer(db: Session, question_id: int, user_answer: str):
    question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not question:
        print(f"Question with ID {question_id} not found")  # Log this for debugging
        raise ValueError("Question not found")
    if question.correct_answer == user_answer:
        return 1
    return 0
