from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    username = Column(String,unique=True)
    password = Column(String,nullable=False)
    games = relationship("Game", back_populates="owner")
class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String,nullable=False)
    option_a = Column(String,nullable=False)
    option_b = Column(String,nullable=False)
    option_c = Column(String,nullable=False)
    option_d = Column(String,nullable=False)
    correct_answer = Column(String)  # a, b, c, d
    difficulty = Column(String,nullable=False)  # easy, medium, hard


# Tabelul Game

class Game(Base):
    __tablename__ = "game"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    score = Column(Float, default=0)  # scorul jucatorului
    difficulty = Column(String, nullable=False)  # dificultatea
    owner = relationship("User", back_populates="games")
    current_question_id = Column(Integer, ForeignKey("questions.id"))
    player = relationship("User", back_populates="games")
    current_question = relationship("Question")
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

    # Relatie
    current_question = Column(Integer, nullable=True)  # Stocam intrebarea curenta

