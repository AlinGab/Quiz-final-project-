from sqlalchemy.orm import Session

from . import models, schemas

#Function to get a user from db
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

#Function to search the username
def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.username == name).first()


#Function to create a user
def create_user(db: Session, user: schemas.UserCreate):
    password = user.password
    db_user = models.User(username=user.username,name = user.name, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db.query(models.User).filter_by(id=user_id).delete()
    db.commit()

# Gets the quiz from the database by ID
def get_game_with_player_name(db: Session, current_question_id: int, user_id: int):
    return db.query(models.Game).filter(models.Game.current_question_id == current_question_id, models.Game.user_id == user_id).first()

# Function to create a game
def create_game_for_player(db: Session, user_id: int,  difficulty: str):
    new_game = models.Game(user_id=user_id,  difficulty=difficulty)
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return new_game

def delete_current_game(db: Session, user_id: int):
    db.query(models.Game).filter_by(id=user_id).delete()
    db.commit()
