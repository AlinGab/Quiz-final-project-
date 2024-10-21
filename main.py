from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from database import SessionLocal, engine
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import bcrypt
import random


app = FastAPI()

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authentication handler
def get_login(
    credentials: HTTPBasicCredentials = Depends(HTTPBasic()),
    db: Session = Depends(get_db)
) -> models.User:
    user = crud.get_user_by_username(db, username=credentials.username)
    if user is None or not bcrypt.checkpw(credentials.password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

# Root endpoint
@app.get("/")
async def root():
    return {"Greeting": "Welcome to our quiz!"}

# User management endpoints
@app.post("/users", response_model=schemas.UserCreate)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db), response: models.User = Depends(get_login)):
    if response is None:
        raise HTTPException(status_code=403, detail="Failed authentication")
    db_user = crud.get_user(db, user_id=response.id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/user/{user_id}")
def delete_current_user(user_id: int, db: Session = Depends(get_db), response: bool = Depends(get_login)):
    if response is None:
        raise HTTPException(status_code=403, detail="Failed authentication")
    crud.delete_user(db, user_id)
    return "User deleted successfully"

# Game management endpoints
@app.post("/users/{user_id}/games/")
def create_game(user_id: int, game: schemas.GameCreate, db: Session = Depends(get_db),
                response: bool = Depends(get_login)):
    if response is None:
        raise HTTPException(status_code=403, detail="Failed authentication")
    try:
        new_game = crud.create_game_for_player(db, user_id, game.difficulty, game.name)

        # Return only the relevant information
        return {
            "id": new_game.id,
            "user_id": new_game.user_id,
            "difficulty": new_game.difficulty,
            "name": new_game.name,
            "score": new_game.score,
            "current_question": new_game.current_question,
            # Add other fields as necessary
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating game: {e}")

@app.get("/games/{game_id}", response_model=schemas.Game)
def get_game(game_id: int, db: Session = Depends(get_db), response: bool = Depends(get_login)):
    if response is None:
        raise HTTPException(status_code=403, detail="Failed authentication")
    db_game = crud.get_game_by_id_and_user(db, game_id, response.id)
    if db_game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return db_game


@app.post("/get-current-question/")
def get_current_question(difficulty: int, user: models.User = Depends(get_login), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=403, detail="Failed authentication")

    # Map difficulty integer to string
    difficulty_map = {
        1: 'easy',
        2: 'medium',
        3: 'hard'
    }

    if difficulty not in difficulty_map:
        raise HTTPException(status_code=400, detail="Invalid difficulty level")

    selected_difficulty = difficulty_map[difficulty]

    # Fetch all questions by difficulty
    questions = crud.get_questions_by_difficulty(db, selected_difficulty)

    if not questions or len(questions) < 5:
        raise HTTPException(status_code=404, detail="Not enough questions available.")

    # Randomly select 5 questions from the available ones
    selected_questions = random.sample(questions, 5)

    return {
        "questions": [
            {
                "id": question.id,
                "question": question.question,  # Ensure this is the correct column name
                "options": {
                    "A": question.option_a,
                    "B": question.option_b,
                    "C": question.option_c,
                    "D": question.option_d,
                }
            }
            for question in selected_questions
        ]
    }


@app.delete("/game/{game_id}")
def delete_current_game(game_id: int, db: Session = Depends(get_db), response: bool = Depends(get_login)):
    if response is None:
        raise HTTPException(status_code=403, detail="Failed authentication")
    crud.delete_current_game(db, game_id)
    return "Game deleted successfully"
