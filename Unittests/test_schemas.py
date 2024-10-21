import pytest
from schemas import UserCreate, QuestionCreate, GameCreate

def test_user_create_schema():
    user_data = {
        "username": "testuser",
        "password": "testpass"
    }
    user = UserCreate(**user_data)
    assert user.username == "testuser"
    assert user.password == "testpass"

def test_invalid_user_schema():
    with pytest.raises(ValueError):
        UserCreate(username="testuser")  # missing pass

def test_question_create_schema():
    question_data = {
        "question": "What is 2 + 2?",
        "option_a": "3",
        "option_b": "4",
        "option_c": "5",
        "option_d": "6",
        "correct_answer": "b",
        "difficulty": "easy"
    }
    question = QuestionCreate(**question_data)
    assert question.question == "What is 2 + 2?"
    assert question.correct_answer == "b"

def test_invalid_question_schema():
    with pytest.raises(ValueError):
        QuestionCreate(  #missing fields
            question="What is 2 + 2?",
            option_a="3",
            option_b="4"
        )

def test_game_create_schema():
    game_data = {
        "score": 0,
        "current_question_id": 1,
        "user_id": 1
    }
    game = GameCreate(**game_data)
    assert game.score == 0
    assert game.current_question_id == 1
