# here we will create the SQLite connection and configuration
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL's connection to SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db" #if we want to change the Database name before the ".db" we change the name

# Create the connection to the database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

#Creating Sesions
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# Base class to get the models
Base = declarative_base()


# this is how we connect our database: it's the same always these lines of code
def get_db():
    db = SessionLocal()
    try:
        yield db  # It gives the sesion to the function that needs it.
    finally:
        db.close() # When the route end responding. it shuts the connection down in a safe way.

# our temporal Database was this one while we were practicing without postgreSQL or similar:
# PRACTICE_DB = [
#     {"id": 1, "name": "Mecanic Keyboard", "price": 75.0, "is_offer": True},
#     {"id": 2, "name": "Logitech g305", "price": 45.5, "is_offer": False},
# ]

