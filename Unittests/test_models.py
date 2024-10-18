import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import SessionLocal, engine
import models

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

def test_user_model(db_session):
    user = models.User(username="testuser", password="testpass")
    db_session.add(user)
    db_session.commit()
    assert user.id is not None
    assert user.username == "testuser"

def test_question_model(db_session):
    question = models.Question(
        question="What is 2 + 2?",
        option_a="3",
        option_b="4",
        option_c="5",
        option_d="6",
        correct_answer="b",
        difficulty="easy"
    )
    db_session.add(question)
    db_session.commit()
    assert question.id is not None

def test_game_model(db_session):
    user = models.User(username="testuser", password="testpass")
    db_session.add(user)
    db_session.commit()

    game = models.Game(name="testuser", difficulty="easy")
    db_session.add(game)
    db_session.commit()
    assert game.id is not None

def test_game_retrieval_by_id(db_session):
    user = models.User(username="testuser", password="testpass")
    db_session.add(user)
    db_session.commit()

    game = models.Game(name="testuser", difficulty="easy")
    db_session.add(game)
    db_session.commit()

    retrieved_game = db_session.query(models.Game).filter(models.Game.id == game.id).first()
    assert retrieved_game.id == game.id
