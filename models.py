from sqlalchemy import Column, Integer, Float, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base

# User Model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    name = Column(String)

    games = relationship("Game", back_populates="user")
    scores = relationship("UserScore", back_populates="user")  # Link to UserScore

# Question Model
class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String, nullable=False)
    option_a = Column(String, nullable=False)
    option_b = Column(String, nullable=False)
    option_c = Column(String, nullable=False)
    option_d = Column(String, nullable=False)
    correct_answer = Column(String)  # a, b, c, d
    difficulty = Column(String, nullable=False)  # easy, medium, hard

# Game Model
class Game(Base):
    __tablename__ = "game"
    id = Column(Integer, primary_key=True, index=True)
    score = Column(Float, default=0)  # Player's score
    difficulty = Column(String, nullable=False)  # Game difficulty
    name = Column(String, nullable=False)  # Player's name

    user_id = Column(Integer, ForeignKey("users.id"))

    # Questions and answers
    question_1 = Column(Integer, ForeignKey("questions.id"))
    answer_1 = Column(String, nullable=True)
    is_correct_1 = Column(Integer, default=0)

    question_2 = Column(Integer, ForeignKey("questions.id"))
    answer_2 = Column(String, nullable=True)
    is_correct_2 = Column(Integer, default=0)

    question_3 = Column(Integer, ForeignKey("questions.id"))
    answer_3 = Column(String, nullable=True)
    is_correct_3 = Column(Integer, default=0)

    question_4 = Column(Integer, ForeignKey("questions.id"))
    answer_4 = Column(String, nullable=True)
    is_correct_4 = Column(Integer, default=0)

    question_5 = Column(Integer, ForeignKey("questions.id"))
    answer_5 = Column(String, nullable=True)
    is_correct_5 = Column(Integer, default=0)

    # Relationship
    current_question = Column(Integer, nullable=True)  # Store the current question ID
    user = relationship("User", back_populates="games")

# UserScore Model
class UserScore(Base):
    __tablename__ = "user_scores"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    game_id = Column(Integer, ForeignKey("game.id"))
    score = Column(Integer, default=0)

    # Relationships
    user = relationship("User", back_populates="scores")
