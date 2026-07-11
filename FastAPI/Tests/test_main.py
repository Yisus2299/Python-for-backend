# Here is we'll create tests is the data is invalid, so we simulate different POSTs
from fastapi.testclient import TestClient
from main import app
import time

client = TestClient(app)

def get_test_token():
    # 1. user data test
    user_data = {
        "email": "test@test.com",
        "password": "test1234"
    }
    
    # 2. try to register the user
    response = client.post("/auth/register", json=user_data)
    
    # 3. if the form fails because it already exists (we ignore it)
    #    if it fails because another reason, we raise an error.
    if response.status_code not in [201, 400]:
        raise Exception(f"Register failed: {response.status_code} - {response.text}")
    
    # 4. now we sign in
    response = client.post("/auth/login", json=user_data)
    
    # 5. if the login fails, we wait and try it again (just in case if the database is slow)
    if response.status_code != 200:
        time.sleep(0.5)  # a pause
        response = client.post("/auth/login", json=user_data)
    
    # 6. if it keep failing, we raise the error
    if response.status_code != 200:
        raise Exception(f"Login failed: {response.status_code} - {response.text}")
    
    # 7. We get the token back
    return response.json()["access_token"]
############################################################

def test_create_product_negative_price():
    # 1. getting the token
    token = get_test_token()
    
    # 2. Create the product payload (data) 
    payload = {
        "name": "T-shirt fail test",
        "price": -15.0,
        "stock": 10,
        "is_offer": False,
        "category_id": 1
    }
    
    # 3. We sent the petition with the authentication
    response = client.post(
        "/products/",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # 4. We verufy if the error is 422 (validation) instead 401 (authentication)
    assert response.status_code == 422
    assert "detail" in response.json()
