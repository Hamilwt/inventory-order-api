from fastapi.testclient import TestClient
from app.main import app

# Create a simulated client to send requests to our app
client = TestClient(app)

def test_get_all_products():
    """Test that the API successfully returns a list of products."""
    response = client.get("/products/")
    
    # 1. Assert that the server responded with a 200 OK status
    assert response.status_code == 200
    
    # 2. Assert that the response body is a list (JSON array)
    assert isinstance(response.json(), list)

def test_prevent_overselling():
    """Test that the API blocks an order when stock is insufficient."""
    # Create a fake order request for 500 laptops
    fake_order = {
        "customer_id": "pytest_user_999",
        "items": [
            {
                "product_id": 1,
                "quantity": 500  # Intentionally impossibly high
            }
        ]
    }
    
    response = client.post("/orders/", json=fake_order)
    
    # Assert that the server caught the error and threw a 400 Bad Request
    assert response.status_code == 400
    
    # Assert that the correct error message was returned
    assert "Not enough stock" in response.json()["detail"]