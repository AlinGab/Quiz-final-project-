from fastapi import Depends, FastAPI,HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
from fastapi.security import HTTPBasic, HTTPBasicCredentials



models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


basic_security = HTTPBasic()


#Creates root for the app
@app.get("/")
async def root():
 return {"Greeting":"Welcome to our quiz!"}

#The log in function
def get_login(
    credentials: HTTPBasicCredentials = Depends(basic_security),
    db: Session = Depends(get_db),
) -> models.User:
    #Checks if the user is already in db
    user = crud.get_user_by_name(db, name=credentials.username)
    #Checks for the data
    if user is None or credentials.password != user.password:
        return None

    return user

# Creates the user name for the game
@app.post("/users", response_model=schemas.UserCreate)
def create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):
    #Checks if the user already exist
    db_user = crud.get_user_by_name(db, name=user.username)
    #If the user is not in db the statement will create a new user
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=user)



@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db),
                response: models.User = Depends(get_login)):
    # Check if user is authenticated
    if response is None:
        raise HTTPException(status_code=403, detail="Failed authentication")
    #Searching for the user in db
    db_user = crud.get_user(db, user_id=response.id)
    #In case the user is not in db
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.delete("/user/{user_id}")
def delete_current_user(user_id: int, db: Session = Depends(get_db),
                response: bool = Depends(get_login)):
    # Check if user is authenticated
    if response is None:
        raise HTTPException(status_code=403, detail="Failed authentication")
    #Deletes the usrer
    crud.delete_user(db, user_id)
    return "User deleted completed"



@app.post("/users/{user_id}/games/")
def create_game(user_id: int, game: schemas.GameCreate, db: Session = Depends(get_db),
                response: bool = Depends(get_login)):
    # Check if user is authenticated
    if response is None:
        raise HTTPException(status_code=403, detail="Failed authentication")
    #Creates the game
    try:
        new_game = crud.create_game_for_player(db, user_id, game.user_id)
        return new_game
    #Raise the error in case you can't create the game and if the game exist already
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating game: {e}")


@app.get("/games/{game_id}", response_model=schemas.Game)
def get_game(game_id: int, db: Session = Depends(get_db), response: bool = Depends(get_login)):
    # Check if user is authenticated
    if response is None:
        raise HTTPException(status_code=403, detail="Failed authentication")
    # Retrieve game with player name (assuming response.id is the user_id)
    db_game = crud.get_game_with_player_name(db, current_question_id=game_id, user_id=response.id)
    # Check if the game exists
    if db_game is None:
        raise HTTPException(status_code=404, detail="Game not found")

    return db_game

@app.post("/games/{game_id}/play")
def play_game(game_id: int, answer: str, db: Session = Depends(get_db),
              response: models.User = Depends(get_login)):
    # Check if user is authenticated
    if response is None:
        raise HTTPException(status_code=403, detail="Failed authentication")

    # Fetch the game state
    db_game = crud.get_game_with_player_name(db, current_question_id=game_id, user_id=response.id)
    if db_game is None:
        raise HTTPException(status_code=404, detail="Game not found")

    # Check the current question and compare the answer
    current_question = db_game.current_question_id

    if current_question == db_game.question_1:
        correct_answer = db_game.answer_1
    elif current_question == db_game.question_2:
        correct_answer = db_game.answer_2
    elif current_question == db_game.question_3:
        correct_answer = db_game.answer_3
    elif current_question == db_game.question_4:
        correct_answer = db_game.answer_4
    elif current_question == db_game.question_5:
        correct_answer = db_game.answer_5
    else:
        raise HTTPException(status_code=400, detail="No more questions in the game.")

    # Validate the user's answer
    is_correct = answer == correct_answer

    # Determine the points based on difficulty
    if db_game.difficulty == "easy":
        points = 5  # For easy, less points
    elif db_game.difficulty == "medium":
        points = 10  # For medium, standard points
    elif db_game.difficulty == "hard":
        points = 20  # For hard, more points
    else:
        points = 10  # Default to medium points if difficulty is unknown

    # Update the score based on correctness
    if is_correct:
        db_game.score += points
    else:
        db_game.score -= points  # Optionally subtract points for incorrect answers

    # Move to the next question (if any)
    if current_question == db_game.question_1:
        db_game.current_question_id = db_game.question_2
    elif current_question == db_game.question_2:
        db_game.current_question_id = db_game.question_3
    elif current_question == db_game.question_3:
        db_game.current_question_id = db_game.question_4
    elif current_question == db_game.question_4:
        db_game.current_question_id = db_game.question_5
    elif current_question == db_game.question_5:
        db_game.current_question_id = None  # No more questions, game finished.

    # Save the game state
    db.commit()
    db.refresh(db_game)

    return {
        "correct": is_correct,
        "new_score": db_game.score,
        "next_question_id": db_game.current_question_id,
        "difficulty": db_game.difficulty,
        "game_finished": db_game.current_question_id is None
    }

@app.delete("/game/{game_id}")
def delete_current_game(user_id: int, db: Session = Depends(get_db),
                    response: bool = Depends(get_login)):
    # Check if user is authenticated
    if response is None:
        raise HTTPException(status_code=403, detail="Failed authentication")
    #Deletes the game
    db_game_del = crud.delete_current_game(db, user_id)
    return "Game deleted completed"
    #Chefk if the game is in db
    if db_game_del is None:
        raise HTTPException(status_code=404, detail="Game not found")
