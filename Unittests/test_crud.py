import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import SessionLocal, engine
import models
import schemas
import crud

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_quiz_game.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
models.Base.metadata.create_all(bind=engine)

@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

def test_create_user(db_session):
    user_data = schemas.UserCreate(username="testuser", password="testpass")
    user = crud.create_user(db_session, user_data)
    assert user.username == user_data.username
    assert user.password == user_data.password

def test_get_user(db_session):
    user_data = schemas.UserCreate(username="testuser", password="testpass")
    crud.create_user(db_session, user_data)
    user = crud.get_user(db_session, 1)
    assert user.username == "testuser"

def test_get_user_by_username(db_session):
    user_data = schemas.UserCreate(username="testuser", password="testpass")
    crud.create_user(db_session, user_data)
    user = crud.get_user_by_username(db_session, "testuser")
    assert user.username == "testuser"

def test_duplicate_user_creation(db_session):
    user_data = schemas.UserCreate(username="testuser", password="testpass")
    crud.create_user(db_session, user_data)
    with pytest.raises(Exception):
        crud.create_user(db_session, user_data)

def test_create_game_for_player(db_session):
    user_data = schemas.UserCreate(username="testuser", password="testpass")
    user = crud.create_user(db_session, user_data)
    game = crud.create_game_for_player(db_session, user.id, "testuser", "easy")
    assert game.name == "testuser"
    assert game.difficulty == "easy"

def test_update_game_with_answers(db_session):
    user_data = schemas.UserCreate(username="testuser", password="testpass")
    user = crud.create_user(db_session, user_data)
    game = crud.create_game_for_player(db_session, user.id, "testuser", "easy")
    question_ids = [1, 2, 3, 4, 5]
    answers = ["a", "b", "c", "d", "a"]
    correctness = [1, 0, 1, 0, 1]
    updated_game = crud.update_game_with_answers(db_session, game.id, question_ids, answers, correctness)
    assert updated_game.answer_1 == "a"
    assert updated_game.is_correct_2 == 0


