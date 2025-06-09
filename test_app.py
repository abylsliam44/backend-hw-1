import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_app():
    # 1. Register a new user
    register_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123"
    }
    
    print("\n1. Registering new user...")
    response = requests.post(f"{BASE_URL}/register", json=register_data)
    print(f"Response: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

    # 2. Login
    print("\n2. Logging in...")
    login_data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    response = requests.post(
        f"{BASE_URL}/token",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    print(f"Response: {response.status_code}")
    token_data = response.json()
    print(json.dumps(token_data, indent=2))

    # Set up headers with token
    headers = {
        "Authorization": f"Bearer {token_data['access_token']}",
        "Content-Type": "application/json"
    }

    # 3. Get user info
    print("\n3. Getting user info...")
    response = requests.get(f"{BASE_URL}/me", headers=headers)
    print(f"Response: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

    # 4. Create a new transaction
    print("\n4. Creating a new transaction...")
    transaction_data = {
        "amount": 1000.50,
        "type": "income",
        "description": "Monthly salary",
        "category_id": 1,  # Assuming category ID 1 exists (Salary)
        "date": datetime.now().isoformat()
    }
    response = requests.post(f"{BASE_URL}/transactions", headers=headers, json=transaction_data)
    print(f"Response: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

    # 5. Create a budget
    print("\n5. Creating a new budget...")
    budget_data = {
        "amount": 500.00,
        "month": datetime.now().month,
        "year": datetime.now().year,
        "category_id": 5  # Assuming category ID 5 exists (Groceries)
    }
    response = requests.post(f"{BASE_URL}/budgets", headers=headers, json=budget_data)
    print(f"Response: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

    # 6. Get dashboard summary
    print("\n6. Getting dashboard summary...")
    response = requests.get(f"{BASE_URL}/dashboard", headers=headers)
    print(f"Response: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    test_app() 