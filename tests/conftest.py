from fastapi.testclient import TestClient
import pytest
from app.main import app
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.database import Base,get_db
from app.models import User
from app import utils
from app.oauth2 import create_access_token
from app import models

# testing database

SQLALCHEMY_DATABASE_URL="postgresql://postgres:Shiva%402005@localhost:5432/test_expense"
engine=create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal=sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False

)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():

    db=TestingSessionLocal()
    try:
        yield db

    finally:
        db.close()  

app.dependency_overrides[get_db]=override_get_db 

# create db sessions whenever required

@pytest.fixture
def test_db():
    db=TestingSessionLocal()
    try:
     yield db
    finally:
     db.close()  
          

@pytest.fixture
def test_client():
    with TestClient(app) as client:
        yield client

@pytest.fixture
def test_user1(test_db):

    user1=models.User(
        email="spal13138@gmail.com",
        password=hash("123345678")
    )

    test_db.add(user1)

    test_db.commit()

    test_db.refresh(user1)
    
    return user1

@pytest.fixture
def test_user2(test_db):

    user2=models.User(
        email="rohit13138@gmail.com",
        password=hash("1233412312")
    )

    test_db.add(user2)

    test_db.commit()

    test_db.refresh(user2)
    
    return user2


@pytest.fixture
def authorization_token1(test_user1):
   
   token=create_access_token(
      {"user_id":test_user1.id}
   )

   return token


@pytest.fixture
def authorization_token2(test_user2):
   
   token=create_access_token(
      {"user_id":test_user2.id}
   )

   return token



@pytest.fixture
def authorized_client1(test_client,authorization_token1):
    with TestClient(app) as client:
        client.headers.update(
        {
        "Authorization":f"Bearer {authorization_token1}"
        }
    )

    return client

@pytest.fixture
def authorized_client2(test_client,authorization_token2):
    test_client.headers.update(
       {
          "Authorization":f"Bearer {authorization_token2}"
       }
    )

    return test_client

@pytest.fixture
def test_expense(test_db, test_user1):

    expense = models.Expense(
        title="Food",
        amount=500,
        category="Food",
        description="Lunch",
        owner_id=test_user1.id
    )

    test_db.add(expense)

    test_db.commit()

    test_db.refresh(expense)

    return expense





