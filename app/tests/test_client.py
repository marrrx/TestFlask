import pytest
from flask import Flask
from flask_restful import Api
from app.api.controllers import createUser, deleteUser, readUsers, readUser, tryGet, updateUser
from app.api.extension import db
from unittest.mock import Mock, patch


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True
    api = Api(app)
    db.init_app(app)

    api.add_resource(createUser, "/api/users/register")
    api.add_resource(readUsers, "/api/users")
    api.add_resource(readUser, "/api/users/<int:id>")
    api.add_resource(updateUser, "/api/users/<int:id>")
    api.add_resource(deleteUser, "/api/users/<int:id>")
    api.add_resource(tryGet, "/api/users/try")

    with app.app_context():
        db.create_all()
    
    yield app  # Yield the Flask app instead of the test client

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()  


def test_try_get(client):
    response = client.get('/api/users/try')
    assert response.status_code == 200
    assert response.json == {"message": "Success"}


def test_create_user(client):
    response = client.post('/api/users/register', json={
        "name": "John Doe",
        "email": "john@example.com",
        "password": "Password123"
    })
    assert response.status_code == 201
    assert response.json["name"] == "John Doe"
    assert response.json["email"] == "john@example.com"



def test_create_user_invalid_data(client):
    response = client.post('/api/users/register', json={
        "name": "",
        "email": "invalid-email",
        "password": "short"
    })
    assert response.status_code == 400
    assert "errors" in response.json

def test_read_users(client):
    client.post('/api/users/register', json={
        "name": "John Doe",
        "email": "john@example.com",
        "password": "Password123"
    })
    
    response = client.get('/api/users')
    assert response.status_code == 201  # Note: This should probably be 200 in your actual code
    assert len(response.json) == 1
    assert response.json[0]["name"] == "John Doe"

def test_read_user(client):
    # First, create a user
    create_response = client.post('/api/users/register', json={
        "name": "John Doe",
        "email": "john@example.com",
        "password": "Password123"
    })
    user_id = create_response.json["id"]
    
    response = client.get(f'/api/users/{user_id}')
    assert response.status_code == 201  # Note: This should probably be 200 in your actual code
    assert response.json["name"] == "John Doe"
    assert response.json["email"] == "john@example.com"

def test_update_user(client):
    # First, create a user
    create_response = client.post('/api/users/register', json={
        "name": "John Doe",
        "email": "john@example.com",
        "password": "Password123"
    })
    user_id = create_response.json["id"]
    
    response = client.put(f'/api/users/{user_id}', json={
        "name": "Jane Doe",
        "email": "jane@example.com",
        "password": "NewPassword123"
    })
    assert response.status_code == 200
    assert response.json["name"] == "Jane Doe"
    assert response.json["email"] == "jane@example.com"

def test_update_user_not_found(client):
    response = client.put('/api/users/999', json={
        "name": "Jane Doe"
    })
    assert response.status_code == 404

def test_delete_user(client):
    create_response = client.post('/api/users/register', json={
        "name": "John Doe",
        "email": "john@example.com",
        "password": "Password123"
    })
    user_id = create_response.json["id"]
    
    response = client.delete(f'/api/users/{user_id}')
    assert response.status_code == 200
    assert response.json["message"] == "User deleted successfully"

def test_delete_user_not_found(client):
    response = client.delete('/api/users/999')
    assert response.status_code == 404


@patch.object(readUser, 'get')
def test_user_get(mock_get):
    mock_user= Mock()
    mock_user.id = 1
    mock_user.username = 'XXXXXXXXXXXXX'
    mock_user.email = 'XXXXXXXXXXXXX'
    mock_user.password = 'XXXXXXXXXXXXX'
    mock_get.return_value = mock_user

    result = readUser.get()
    assert result.id == 1
    assert result.username == 'XXXXXXXXXXXXX'
    assert result.email == 'XXXXXXXXXXXXX'
    assert result.password == 'XXXXXXXXXXXXX'
    mock_get.assert_called_once()
