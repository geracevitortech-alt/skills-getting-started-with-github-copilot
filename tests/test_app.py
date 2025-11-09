import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert response.json() == activities
    assert "Chess Club" in response.json()
    assert "Programming Class" in response.json()

def test_signup_new_student():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in activities[activity_name]["participants"]

def test_signup_existing_student():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already in Chess Club
    
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert response.status_code == 400
    assert response.json() == {"detail": "Student is already signed up"}

def test_signup_nonexistent_activity():
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}

def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200  # Success status code with redirect response
    assert response.url.path == "/static/index.html"  # Check final redirected URL

def test_activity_data_structure():
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_name, str)
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        assert isinstance(activity_data["participants"], list)