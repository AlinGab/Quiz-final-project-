from sqlalchemy.orm import Session
import models
import schemas
import bcrypt

# User Operations
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db_user = models.User(username=user.username, password=hashed_password, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db.query(models.User).filter_by(id=user_id).delete()
    db.commit()

# Game Operations
def get_game_by_id_and_user(db: Session, game_id: int, user_id: int):
    return db.query(models.Game).filter(
        models.Game.id == game_id,
        models.Game.user_id == user_id
    ).first()

def get_game_with_player_name(db: Session, current_question_id: int, user_id: int):
    return db.query(models.Game).filter(models.Game.current_question_id == current_question_id, models.Game.user_id == user_id).first()


def create_game_for_player(db: Session, user_id: int, difficulty: str, name: str):
    new_game = models.Game(
        user_id=user_id,
        difficulty=difficulty,
        name=name,
        score=0,
        current_question=None,  # or some default value
        question_1=None,
        question_2=None,
        question_3=None,
        question_4=None,
        question_5=None,
        answer_1=None,
        answer_2=None,
        answer_3=None,
        answer_4=None,
        answer_5=None,
        is_correct_1=0,
        is_correct_2=0,
        is_correct_3=0,
        is_correct_4=0,
        is_correct_5=0,
    )

    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return new_game


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


def get_questions_by_difficulty(db: Session, difficulty: str):
    return db.query(models.Question).filter(models.Question.difficulty == difficulty).all()



# Delete Current Game
def delete_current_game(db: Session, game_id: int):
    db.query(models.Game).filter_by(id=game_id).delete()
    db.commit()
