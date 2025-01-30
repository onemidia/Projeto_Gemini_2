from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session, scoped_session
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()

def init_db():
    from models import Produto  # Importe o modelo aqui dentro
    Base.metadata.create_all(bind=engine)

def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()