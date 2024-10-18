
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import bcrypt
import random

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
basic_security = HTTPBasic()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authentication handler
def get_login(
        credentials: HTTPBasicCredentials = Depends(basic_security),
        db: Session = Depends(get_db)
) -> models.User:
    user = crud.get_user_by_name(db, username=credentials.username)
    if user is None or not bcrypt.checkpw(credentials.password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

# Submit an answer and return the next question or final score
@app.post("/submit-answer/", response_model=schemas.SubmitAnswerResponse)
async def submit_answer(
        answer_request: schemas.SubmitAnswerRequest,
        user: models.User = Depends(get_login),
        db: Session = Depends(get_db)
):
    game = crud.get_game_by_id_and_user(db, answer_request.game_id, user.id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Validate the answer
    try:
        score_increment = crud.validate_answer(db, answer_request.question_id, answer_request.user_answer)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    # Update the game score
    crud.update_game_score(db, game, score_increment)

    # Update answered questions in the game
    # This depends on how you're tracking answered questions in the Game model
    # For simplicity, let's assume we keep track of answered question IDs in a list
    # You might need to adjust this part according to your actual implementation

    answered_question_ids = [answer_request.question_id]  # You need to manage this list appropriately

    remaining_questions = crud.get_remaining_questions_by_difficulty(
        db, game.difficulty, answered_question_ids)

    if remaining_questions:
        next_question = random.choice(remaining_questions)
        crud.update_game_current_question(db, game, next_question.id)
        return schemas.SubmitAnswerResponse(
            message="Answer processed",
            next_question=schemas.Question(
                id=next_question.id,
                question_text=next_question.question_text,
                correct_answer=next_question.correct_answer,
                difficulty=next_question.difficulty
            )
        )

    return schemas.SubmitAnswerResponse(
        message="Game over",
        final_score=game.score
    )
