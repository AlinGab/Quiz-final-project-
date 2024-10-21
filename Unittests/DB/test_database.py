import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from Final_version.models import Base

# Set up the database for testing
DATABASE_URL = "sqlite:///./quiz_game.db"


@pytest.fixture(scope='module')
def test_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_sample(test_db):
    assert test_db is not None

def test_database_connection(test_db: Session):
    assert test_db is not None

def test_session_lifecycle(test_db: Session):
    assert test_db.bind is not None
