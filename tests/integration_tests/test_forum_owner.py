import pytest
from starlette.testclient import TestClient

from tests.integration_tests.mock_users_data import *
from main import app

@pytest.fixture
def client():
    return TestClient(app)


@pytest.mark.asyncio
async def test_promote_unauthenticated(client):
    # Arrange & Act
    response = client.put('/owner_panel/promote/30')

    # Assert
    assert response.status_code == 401
    assert response.json()["detail"] == NOT_AUTHENTICATED

@pytest.mark.asyncio
async def test_promote_authenticated_as_user(client):
    # Arrange & Act
    jwt_token = user_mock()
    response = client.put('/owner_panel/promote/30', headers={"Authorization": f"Bearer {jwt_token}"})

    # Assert
    assert response.status_code == 403
    assert response.json()["detail"] == NOT_AUTHORIZED

@pytest.mark.asyncio
async def test_promote_authenticated_as_admin(client):
    # Arrange & Act
    jwt_token = admin_mock()
    response = client.put('/owner_panel/promote/30', headers={"Authorization": f"Bearer {jwt_token}"})

    # Assert
    assert response.status_code == 403
    assert response.json()["detail"] == NOT_AUTHORIZED

@pytest.mark.asyncio
async def test_promote_authenticated_as_owner(client):
    # Arrange & Act
    jwt_token = owner_mock()
    response = client.put('/owner_panel/promote/30', headers={"Authorization": f"Bearer {jwt_token}"})

    # Assert
    if response.status_code == 201:
        assert isinstance(response.json(), dict)
    else:
        assert response.status_code == 404

@pytest.mark.asyncio
async def test_demote_unauthenticated(client):
    # Arrange & Act
    response = client.put('/owner_panel/demote/30')

    # Assert
    assert response.status_code == 401
    assert response.json()["detail"] == NOT_AUTHENTICATED

@pytest.mark.asyncio
async def test_demote_authenticated_as_user(client):
    # Arrange & Act
    jwt_token = user_mock()
    response = client.put('/owner_panel/demote/30', headers={"Authorization": f"Bearer {jwt_token}"})

    # Assert
    assert response.status_code == 403
    assert response.json()["detail"] == NOT_AUTHORIZED

@pytest.mark.asyncio
async def test_demote_authenticated_as_admin(client):
    # Arrange & Act
    jwt_token = admin_mock()
    response = client.put('/owner_panel/demote/30', headers={"Authorization": f"Bearer {jwt_token}"})

    # Assert
    assert response.status_code == 403
    assert response.json()["detail"] == NOT_AUTHORIZED

@pytest.mark.asyncio
async def test_demote_authenticated_as_owner(client):
    # Arrange & Act
    jwt_token = owner_mock()
    response = client.put('/owner_panel/demote/30', headers={"Authorization": f"Bearer {jwt_token}"})

    # Assert
    if response.status_code == 201:
        assert isinstance(response.json(), dict)
    else:
        assert response.status_code == 404

@pytest.mark.asyncio
async def test_delete_admin_unauthenticated(client):
    # Arrange & Act
    response = client.delete('/owner_panel/30')

    # Assert
    assert response.status_code == 401
    assert response.json()["detail"] == NOT_AUTHENTICATED

@pytest.mark.asyncio
async def test_delete_admin_authenticated_as_user(client):
    # Arrange & Act
    jwt_token = user_mock()
    response = client.delete('/owner_panel/30',
                             headers={"Authorization": f"Bearer {jwt_token}"})

    # Assert
    assert response.status_code == 403
    assert response.json()["detail"] == NOT_AUTHORIZED

@pytest.mark.asyncio
async def test_delete_admin_authenticated_as_admin(client):
    # Arrange & Act
    jwt_token = admin_mock()
    response = client.delete('/owner_panel/30',
                             headers={"Authorization": f"Bearer {jwt_token}"})

    # Assert
    assert response.status_code == 403
    assert response.json()["detail"] == NOT_AUTHORIZED


@pytest.mark.asyncio
async def test_delete_admin_authenticated_as_owner(client):
    # Arrange & Act
    jwt_token = owner_mock()
    response = client.delete('/owner_panel/30',
                             headers={"Authorization": f"Bearer {jwt_token}"})

    # Assert
    if response.status_code == 204:
        assert isinstance(response.json(), dict)
    else:
        assert response.status_code == 404