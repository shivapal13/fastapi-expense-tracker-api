import pytest
from fastapi.testclient import TestClient
from app.main import app
from fastapi import status


def test_get(authorized_client1):

    response=authorized_client1.get ("/expense")

    assert response.status_code==status.HTTP_200_OK

def test_get_all_expenses(authorized_client1,test_expense):


    response = authorized_client1.get(
        "/expense"
    )

    assert response.status_code == status.HTTP_200_OK

def test_get_single_expense(
    authorized_client1,
    test_expense
):

    response = authorized_client1.get(
        f"/expense/{test_expense.id}"
    )

    assert response.status_code == status.HTTP_200_OK

def test_create_expense(authorized_client1):

    test_create_expense={
        "title":"travel",
        "amount":50,
        "category":"travel",
        "description":"payment online"
    }
 
    response=authorized_client1.post("/expense",json=test_create_expense)

    assert response.status_code==status.HTTP_201_CREATED

    data=response.json()

    assert data["title"]=="travel"
    assert data["amount"]==50

def test_update_expense(authorized_client1):

    response=authorized_client1.post("/expense",json={
                    "title" :"education",
                    "amount":500,
                    "category":"updated data",
                    "description":"payment will occur through online"    
                    })
    
    created_expense=response.json()
    
    
    
    updated_data = {
        "title":"updated grocery",
        "amount":800,
        "category":"food",
        "description":"updated payment"
    }
    response = authorized_client1.put(
        (f"/expense/{created_expense['id']}"),
        json=updated_data
    )

    assert response.status_code == status.HTTP_200_OK

def test_update_non_existing_expense(
    authorized_client1
):

    updated_data = {
        "title":"updated",
        "amount":800,
        "category":"Food",
        "description":"updated payment"
    }

    response = authorized_client1.put(
        "/expense/999",
        json=updated_data
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_expense(authorized_client1):
        response=authorized_client1.post("/expense",json={
            "title" :"education",
            "amount":500,
            "category":"updated data",
            "description":"payment will occur through online"    
        })
    
        created_expense=response.json()


        response=authorized_client1.delete(f"/expense/{created_expense['id']}")
        assert response.status_code==status.HTTP_204_NO_CONTENT

def test_delete_non_existing_expense(
    authorized_client1
):

    response = authorized_client1.delete(
        "/expense/999"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_invalid_expense(authorized_client1):
     
    expense_data={
          "title":"hello",
          "amount":-500,
          "category":"food",
          "description":5666
    
    }
     
    response=authorized_client1.post("/expense",json=expense_data)

    assert response.status_code==status.HTTP_422_UNPROCESSABLE_CONTENT


def test_ownership_relation(authorized_client1,authorized_client2):

    response=authorized_client1.post("/expense",json={
         "title" :"education",
            "amount":500,
            "category":"updated data",
            "description":"payment will occur through online"  
    })  

    expense=response.json()

    response=authorized_client2.delete(f"/expense/{expense['id']}")

    assert response.status_code==status.HTTP_403_FORBIDDEN
