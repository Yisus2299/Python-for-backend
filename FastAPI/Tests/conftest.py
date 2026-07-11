# here we will create the Database tests

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

# 1- we create the engine aiming to updating and improving the RAM memory

SQLALCHEMY_DATABSE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABSE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autommit = False, autoflush=False, bind=engine)

# 2- we include Fixture which prepares Tables before every single test and it deleetes everything once is finished
@pytest.fixture(scope="function")
def db_session():
    # it creates all tables in their models into the temporal database
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        #it deletes everything at the end of the tests, it cleans everything for the next tests
        Base.metadata.drop_all(bind=engine)

# fixture that overwrittes the dependency "get_db" in our app
@pytest.fixture(scope="function")
def client(db_session):
    def _get_test_db():
        try:
            yield db_session
        finally:
            pass
        
        # Inyect the test database in FastAPI
        app.dependency_overrides[get_db] = _get_test_db
        from fastapi.testclient import TestClient
        # at the end of tests, clean the override to don't affect the real app
        app.dependy_overrides.clear()