import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Final_version.database import Base, SessionLocal
from Final_version.main import app


SQLALCHEMY_DATABASE_URL = "sqlite:///./quiz_game.db"  # Use SQLite for testing
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})


Base.metadata.create_all(bind=engine)


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def test_client():
    client = TestClient(app)
    yield client


@pytest.fixture(scope="function")
def db_session():
    db = TestingSessionLocal()
    yield db
    db.close()


# Test for root endpoint
def test_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Greeting": "Welcome to our quiz!"}


# Test for creating a user
def test_create_user(test_client, db_session):
    response = test_client.post("/users", json={"username": "testuser", "password": "testpass", "name": "Test User"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


# Test for reading a user
def test_read_user(test_client, db_session):
    # Create a user first
    test_client.post("/users", json={"username": "testuser2", "password": "testpass2", "name": "Test User 2"})

    response = test_client.get("/users/1", auth=("testuser2", "testpass2"))
    assert response.status_code == 200
    assert response.json()["username"] == "testuser2"


# Test for user not found
def test_read_user_not_found(test_client):
    response = test_client.get("/users/999", auth=("testuser123", "testpass"))
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_create_game(test_client, db_session):

    response_create_user = test_client.post("/users", json={
        "username": "testuser",
        "password": "testpass",
        "name": "Test User"
    })

    assert response_create_user.status_code == 200 or response_create_user.status_code == 400


    response = test_client.post("/users/6/games/", json={
        "name": "Test Game",
        "difficulty": "easy",
        "score": 0,
        "user_id": 6
    },
    auth=("testuser", "testpass"))


    print(response.json())

    assert response.status_code == 200



# Test for game not found
def test_get_game_not_found(test_client):
    response = test_client.get("/games/999", auth=("testuser", "testpass"))
    assert response.status_code == 404
    assert response.json()["detail"] == "Game not found"


# Test for getting current question
def test_get_current_question(test_client):
    response = test_client.post("/get-current-question/", json={"difficulty": 1}, auth=("testuser", "testpass"))
    assert response.status_code == 200
    assert "questions" in response.json()


# Test for submitting answers
def test_submit_answers(test_client):
    # Create a game for the user first
    test_client.post("/users", json={"username": "testuser4", "password": "testpass4", "name": "Test User 4"})
    test_client.post("/users/1/games/", json={"name": "Test Game 2", "difficulty": "easy"},
                     auth=("testuser4", "testpass4"))

    # Assuming a question with ID 1 exists
    response = test_client.post("/submit-answers/", json={
        "game_id": 1,
        "answers": [{"question_id": 1, "user_answer": "A"}]
    }, auth=("testuser4", "testpass4"))

    assert response.status_code == 200
    assert "message" in response.json()


# Test for deleting a user  - Works
def test_delete_user(test_client):
    response = test_client.delete("/user/1", auth=("testuser", "testpass"))
    assert response.status_code == 200
    assert response.json() == "User deleted successfully"


# Test for deleting a game  - Works!
def test_delete_game(test_client):
    # Create a game for the user first
    test_client.post("/users", json={"username": "testuser5", "password": "testpass5", "name": "Test User 5"})
    test_client.post("/users/1/games/", json={"name": "Test Game 3", "difficulty": "easy"},
                     auth=("testuser5", "testpass5"))

    response = test_client.delete("/game/1", auth=("testuser5", "testpass5"))
    assert response.status_code == 200
    assert response.json() == "Game deleted successfully"

