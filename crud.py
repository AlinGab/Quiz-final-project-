from sqlalchemy.orm import Session
import models
import schemas

# aici ar putea fi updatat la codul final

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#########################################


# Functie pentru a obtine jocul unui jucător după ID
def get_game_with_player_name(db: Session, game_id: int):
    return db.query(models.Game).filter(models.Game.id == game_id).first()


# Functie pentru a crea un nou joc
def create_game_for_player(db: Session, user_id: int, player_name: str, difficulty: str):
    new_game = models.Game(user_id=user_id, name=player_name, difficulty=difficulty)
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return new_game


# Functie pentru adaugarea intrebarilor si raspunsurilor
def update_game_with_answers(db: Session, game_id: int, question_ids: list, answers: list, correctness: list):
    game = db.query(models.Game).filter(models.Game.id == game_id).first()

    if game:
        # Adaugam intrebarile si raspunsurile corespunzatoare
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
