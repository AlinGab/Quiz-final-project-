
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import bcrypt
import random
from typing import List
from schemas import SubmitAnswerRequest
# from crud import get_correct_answers_for_game
from schemas import SubmitAnswerResponse
import python_multipart

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


# Submit an answer and return the next question or final score
@app.post("/submit-answers/", response_model=schemas.SubmitAnswerResponse)
async def submit_answers(
        answer_request: schemas.SubmitAnswerRequest,
        user: models.User = Depends(get_login),
        db: Session = Depends(get_db)
):
    game = crud.get_game_by_id_and_user(db, answer_request.game_id, user.id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    # DE AICI PARTEA ASTA DE ADAUGAT

    correct_count = 0
    answered_question_ids = []  # To keep track of answered questions

    # Process all answers in the request body
    for answer in answer_request.answers:
        try:
            # Validate each answer
            score_increment = crud.validate_answer(db, answer.question_id, answer.user_answer)
            crud.update_game_score(db, game, score_increment)
            correct_count += score_increment
            answered_question_ids.append(answer.question_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    # Get the remaining questions for the game
    remaining_questions = crud.get_remaining_questions_by_difficulty(
        db, game.difficulty, answered_question_ids)

    # Update the game score
    crud.update_game_score(db, game, score_increment)

    # Track the answered questions
    answered_question_ids = [answer_request.question_id]
    if remaining_questions:
        # Prompt for the next question if there are still unanswered questions
        next_question = random.choice(remaining_questions)
        crud.update_game_current_question(db, game, next_question.id)
        return schemas.SubmitAnswerResponse(
            message="Answer processed. Here is your next question.",
            next_question=schemas.Question(
                id=next_question.id,
                question_text=next_question.question_text,
                option_a=next_question.option_a,
                option_b=next_question.option_b,
                option_c=next_question.option_c,
                option_d=next_question.option_d,
                difficulty=next_question.difficulty,
                correct_answer=None  # Do not reveal the correct answer yet
            )
        )

    # If all questions are answered, calculate final score and finish the game
    final_score = correct_count / len(answer_request.answers) * 100

    return schemas.SubmitAnswerResponse(
        message=f"All questions answered. Final score: {final_score}",
        final_score=final_score
    )
