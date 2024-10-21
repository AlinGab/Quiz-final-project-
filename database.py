from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# definire baza de date pentru SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./quiz_game.db"

# Creare engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Creare sesiune
#flush este pe off - Modificarile nu vor fi trimise la baza de date automat
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# creare baza modele
Base = declarative_base()


def get_db():
    return None