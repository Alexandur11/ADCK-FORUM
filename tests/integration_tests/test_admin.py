import pytest
from starlette.testclient import TestClient

from models.models import AccessControl
from services.admin_services import get_all_users
from tests.integration_tests.mock_users_data import *
from main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.mark.asyncio
async def test_get_all_users_unauthenticated(client):
    # Arrange & Act
    response = client.get('/admin_panel/users/all')

    # Assert
    assert response.status_code == 401
    assert response.json()["detail"] == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_get_all_authenticated_as_user(client):
    # Arrange & Act
    jwt_token = user_mock()
    response = client.get("/admin_panel/users/all", headers={"Authorization": f"Bearer {jwt_token}"})

    # Assert
    assert response.status_code == 403
    assert response.json()['detail'] == NOT_AUTHORIZED


@pytest.mark.asyncio
async def test_get_all_authenticated_as_admin(client):
    # Arrange & Act
    jwt_token = admin_mock()
    response = client.get("/admin_panel/users/all", headers={"Authorization": f"Bearer {jwt_token}"})

    # Assert
    if response.status_code == 200:
        assert isinstance(get_all_users(), tuple)
    else:
        exc_info = response.json()
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == 'There are currently no users registered!'


@pytest.mark.asyncio
async def test_search_by_id_unauthenticated(client):
    # Arrange & Act
    response = client.get('/admin_panel/users/idsearch/6')

    # Assert
    assert response.status_code == 401
    assert response.json()["detail"] == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_search_by_id_authenticated_as_user(client):
    # Arrange & Act
    jwt_token = user_mock()
    response = client.get('/admin_panel/users/idsearch/6', headers={"Authorization": f"Bearer {jwt_token}"})

    # Assert
    assert response.status_code == 403
    assert response.json()['detail'] == NOT_AUTHORIZED


@pytest.mark.asyncio
async def test_search_by_existing_id_authenticated_as_admin(client):
    # Arrange & Act
    jwt_token = admin_mock()
    response = client.get('/admin_panel/users/idsearch/6', headers={"Authorization": f"Bearer {jwt_token}"})
    user_details = response.json()
    # Assert

    assert response.status_code == 200
    assert isinstance(user_details, list)


@pytest.mark.asyncio
async def test_search_by_Non_existing_id_authenticated_as_admin(client):
    # Arrange & Act
    jwt_token = admin_mock()
    response = client.get('/admin_panel/users/idsearch/1', headers={"Authorization": f"Bearer {jwt_token}"})

    # Assert
    exc_info = response.json()
    assert exc_info["detail"] == USER_NOT_FOUND
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_search_by_username_unauthenticated(client):
    # Arrange & Act
    response = client.get('/admin_panel/users/search/Alex')

    # Assert
    assert response.status_code == 401
    assert response.json()["detail"] == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_search_by_username_authenticated_as_user(client):
    # Arrange & Act
    jwt_token = user_mock()
    response = client.get('/admin_panel/users/search/Alex', headers={"Authorization": f"Bearer {jwt_token}"})

    # Assert
    assert response.status_code == 403
    assert response.json()['detail'] == NOT_AUTHORIZED


@pytest.mark.asyncio
async def test_search_by_existing_username_authenticated_as_admin(client):
    # Arrange & Act
    jwt_token = admin_mock()
    response = client.get('/admin_panel/users/search/Alex', headers={"Authorization": f"Bearer {jwt_token}"})
    user_details = response.json()
    # Assert

    assert response.status_code == 200
    assert isinstance(user_details, list)


@pytest.mark.asyncio
async def test_search_by_Non_existing_username_authenticated_as_admin(client):
    # Arrange & Act
    jwt_token = admin_mock()
    response = client.get('/admin_panel/users/search/0123', headers={"Authorization": f"Bearer {jwt_token}"})

    # Assert
    exc_info = response.json()
    assert exc_info["detail"] == USER_NOT_FOUND
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_all_logged_unauthenticated(client):
    # Arrange & Act
    response = client.get('/admin_panel/users/all/logged_now')

    # Assert
    assert response.status_code == 401
    assert response.json()["detail"] == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_all_logged_authenticated_as_user(client):
    # Arrange & Act
    jwt_token = user_mock()
    response = client.get('/admin_panel/users/all/logged_now', headers={"Authorization": f"Bearer {jwt_token}"})

    # Assert
    assert response.status_code == 403
    assert response.json()["detail"] == NOT_AUTHORIZED


@pytest.mark.asyncio
async def test_all_logged_authenticated_as_admin(client):
    # Arrange & Act
    jwt_token = admin_mock()
    response = client.get('/admin_panel/users/all/logged_now', headers={"Authorization": f"Bearer {jwt_token}"})

    # Assert
    if response.status_code == 200:
        assert isinstance(response.json(), list)
    else:
        assert isinstance(response.json(), dict)



@pytest.mark.asyncio
async def test_is_logged_unauthenticated(client):
    # Arrange & Act
    response = client.get('/admin_panel/users/logged/6')

    # Assert
    assert response.status_code == 401
    assert response.json()["detail"] == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_is_logged_authenticated_as_user(client):
    # Arrange & Act
    jwt_token = user_mock()
    response = client.get('/admin_panel/users/logged/6', headers={"Authorization": f"Bearer {jwt_token}"})

    # Assert
    assert response.status_code == 403
    assert response.json()["detail"] == NOT_AUTHORIZED


# @pytest.mark.asyncio
# async def test_is_logged_authenticated_as_admin(client):
#     # Arrange & Act
#     jwt_token = admin_mock()
#     response = client.get('/admin_panel/users/logged/6', headers={"Authorization": f"Bearer {jwt_token}"})
#
#     # Assert
#     if response.status_code == 200:
#         exc_info = response.json()
#         assert exc_info.value.detail == [True,{'message': 'User is logged in.'}]
#     else:
#         exc_info = response.json()
#         print("checkpoint2")
#         assert exc_info.value.status_code == 404
#         assert exc_info.value.detail == [False,{'message': 'User is logged in.'}]

#
# @pytest.mark.asyncio
# async def test_delete_user_unauthenticated(client):
#     # Arrange & Act
#     response = client.delete('/admin_panel')
#
#     # Assert
#     assert response.status_code == 401
#     assert response.json()['detail'] == NOT_AUTHENTICATED
#
#
# @pytest.mark.asyncio
# async def test_delete_user_authenticated_as_user(client):
#     # Arrange & Act
#     jwt_token = user_mock()
#
#     response = client.delete('/admin_panel/user{user_id}', headers={"Authorization": f"Bearer {jwt_token}"})
#
#     # Assert
#     assert response.status_code == 403
#     assert response.json()['detail'] == NOT_AUTHORIZED
#
#
# @pytest.mark.asyncio
# async def test_delete_user_authenticated_as_admin(client):
#     # Arrange & Act
#     jwt_token = admin_mock()
#     response = client.delete('/admin_panel/user/30', headers={"Authorization": f"Bearer {jwt_token}"})
#
#     # Assert
#     if delete_user_by_id(30):
#         assert response.status_code == 204
#         assert response.json() == {'message': 'User deleted successfully!'}
#     else:
#         exc_info = response.json()
#         assert exc_info["detail"] == USER_NOT_FOUND
#         assert response.status_code == 404


@pytest.mark.asyncio
async def test_lock_topic_by_id_unauthenticated(client):
    # Arrange & Act
    response = client.put('admin_panel/actions/topics/lock/28')

    # Assert
    assert response.status_code == 401
    assert response.json()['detail'] == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_lock_topic_by_id_authenticated_as_user(client):
    # Arrange & Act
    jwt_token = user_mock()
    response = client.put('admin_panel/actions/topics/lock/28', headers={"Authorization": f"Bearer {jwt_token}"})

    # Assert
    assert response.status_code == 403
    assert response.json()['detail'] == NOT_AUTHORIZED


@pytest.mark.asyncio
async def test_lock_topic_by_id_authenticated_as_admin(client):
    # Arrange & Act
    jwt_token = admin_mock()
    response = client.put('admin_panel/actions/topics/lock/28', headers={"Authorization": f"Bearer {jwt_token}"})

    # Assert
    if response.status_code == 200:
        assert isinstance(response.json(), dict)
    else:
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_unlock_topic_by_id_unauthenticated(client):
    # Arrange & Act
    response = client.put('admin_panel/actions/topics/unlock/28')

    # Assert
    assert response.status_code == 401
    assert response.json()['detail'] == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_unlock_topic_by_id_authenticated_as_user(client):
    # Arrange & Act
    jwt_token = user_mock()
    response = client.put('admin_panel/actions/topics/unlock/28', headers={"Authorization": f"Bearer {jwt_token}"})

    # Assert
    assert response.status_code == 403
    assert response.json()['detail'] == NOT_AUTHORIZED


@pytest.mark.asyncio
async def test_unlock_topic_by_id_authenticated_as_admin(client):
    # Arrange & Act
    jwt_token = admin_mock()
    response = client.put('admin_panel/actions/topics/lock/28', headers={"Authorization": f"Bearer {jwt_token}"})

    # Assert
    if response.status_code == 200:
        assert isinstance(response.json(), dict)
    else:
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_unlock_category_by_id_unauthenticated(client):
    # Arrange & Act
    response = client.put('admin_panel/actions/categories/unlock/17')

    # Assert
    assert response.status_code == 401
    assert response.json()['detail'] == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_unlock_category_by_id_authenticated(client):
    # Arrange & Act
    jwt_token = user_mock()
    response = client.put('admin_panel/actions/categories/unlock/17', headers={"Authorization": f"Bearer {jwt_token}"})

    # Assert
    assert response.status_code == 403
    assert response.json()['detail'] == NOT_AUTHORIZED


@pytest.mark.asyncio
async def test_unlock_category_by_id_authenticated_as_admin(client):
    # Arrange & Act
    jwt_token = admin_mock()
    response = client.put('admin_panel/actions/categories/unlock/17', headers={"Authorization": f"Bearer {jwt_token}"})

    # Assert
    if response.status_code == 200:
        assert isinstance(response.json(), dict)
    else:
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_lock_category_by_id_unauthenticated(client):
    # Arrange & Act
    response = client.put('admin_panel/actions/categories/lock/17')

    # Assert
    assert response.status_code == 401
    assert response.json()['detail'] == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_lock_category_by_id_authenticated(client):
    # Arrange & Act
    jwt_token = user_mock()
    response = client.put('admin_panel/actions/categories/lock/17', headers={"Authorization": f"Bearer {jwt_token}"})

    # Assert
    assert response.status_code == 403
    assert response.json()['detail'] == NOT_AUTHORIZED


@pytest.mark.asyncio
async def test_lock_category_by_id_authenticated_as_admin(client):
    # Arrange & Act
    jwt_token = admin_mock()
    response = client.put('admin_panel/actions/categories/lock/17', headers={"Authorization": f"Bearer {jwt_token}"})

    # Assert
    if response.status_code == 200:
        assert isinstance(response.json(), dict)
    else:
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_ban_user_by_id_unauthenticated(client):
    # Arrange & Act
    response = client.put('admin_panel/actions/users/ban/30')

    # Assert
    assert response.status_code == 401
    assert response.json()['detail'] == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_ban_user_by_id_authenticated_as_user(client):
    # Arrange & Act
    jwt_token = user_mock()
    response = client.put('admin_panel/actions/users/ban/30', headers={"Authorization": f"Bearer {jwt_token}"})

    # Assert
    assert response.status_code == 403
    assert response.json()['detail'] == NOT_AUTHORIZED


@pytest.mark.asyncio
async def test_ban_user_by_id_authenticated_as_admin(client):
    # Arrange & Act
    jwt_token = admin_mock()
    response = client.put('admin_panel/actions/users/ban/30', headers={"Authorization": f"Bearer {jwt_token}"})

    # Assert
    if response.status_code == 200:
        assert isinstance(response.json(), dict)
    else:
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_give_write_unauthenticated(client):
    # Arrange & Act
    response = client.put('admin_panel/actions/users/write_access')

    # Assert
    assert response.status_code == 401
    assert response.json()["detail"] == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_give_write_authenticated_as_user(client):
    # Arrange & Act
    jwt_token = user_mock()
    access_control = AccessControl(user_id=30, category_id=17)
    response = client.put('admin_panel/actions/users/write_access',
                          headers={"Authorization": f"Bearer {jwt_token}"}, json=access_control.dict())

    # Assert
    assert response.status_code == 403
    assert response.json()["detail"] == NOT_AUTHORIZED


@pytest.mark.asyncio
async def test_give_write_authenticated_as_admin(client):
    # Arrange & Act
    jwt_token = admin_mock()
    access_control = AccessControl(user_id=30, category_id=17)
    response = client.put('admin_panel/actions/users/write_access',
                          headers={"Authorization": f"Bearer {jwt_token}"},
                          json=access_control.dict())

    # Assert
    if response.status_code == 200:
        assert isinstance(response.json(), dict)
    else:
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_give_read_unauthenticated(client):
    # Arrange & Act
    response = client.put('admin_panel/actions/users/read_access')

    # Assert
    assert response.status_code == 401
    assert response.json()["detail"] == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_give_read_authenticated_as_user(client):
    # Arrange & Act
    jwt_token = user_mock()
    access_control = AccessControl(user_id=30, category_id=17)
    response = client.put('admin_panel/actions/users/read_access',
                          headers={"Authorization": f"Bearer {jwt_token}"}, json=access_control.dict())

    # Assert
    assert response.status_code == 403
    assert response.json()["detail"] == NOT_AUTHORIZED


@pytest.mark.asyncio
async def test_give_read_authenticated_as_admin(client):
    # Arrange & Act
    jwt_token = admin_mock()
    access_control = AccessControl(user_id=30, category_id=17)
    response = client.put('admin_panel/actions/users/read_access',
                          headers={"Authorization": f"Bearer {jwt_token}"}, json=access_control.dict())

    # Assert
    if response.status_code == 200:
        assert isinstance(response.json(), dict)
    else:
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_revoke_access_unauthenticated(client):
    # Arrange & Act
    response = client.put('admin_panel/actions/users/no_access')

    # Assert
    assert response.status_code == 401
    assert response.json()["detail"] == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_revoke_access_authenticated_as_user(client):
    # Arrange & Act
    jwt_token = user_mock()
    access_control = AccessControl(user_id=30, category_id=17)
    response = client.put('admin_panel/actions/users/no_access',
                          headers={"Authorization": f"Bearer {jwt_token}"}, json=access_control.dict())

    # Assert
    assert response.status_code == 403
    assert response.json()['detail'] == NOT_AUTHORIZED


@pytest.mark.asyncio
async def test_revoke_access_authenticated_as_admin(client):
    # Arrange & Act
    jwt_token = admin_mock()
    access_control = AccessControl(user_id=30, category_id=17)
    response = client.put('admin_panel/actions/users/no_access',
                          headers={"Authorization": f"Bearer {jwt_token}"}, json=access_control.dict())

    # Assert
    if response.status_code == 200:
        assert isinstance(response.json(), dict)
    else:
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_category_members_unauthenticated(client):
    # Arrange & Act
    response = client.get('admin_panel/actions/categories/members/17')

    # Assert
    assert response.status_code == 401
    assert response.json()["detail"] == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_category_members_authenticated_as_user(client):
    # Arrange & Act
    jwt_token = user_mock()
    response = client.get('admin_panel/actions/categories/members/17',
                          headers={"Authorization": f"Bearer {jwt_token}"})

    # Assert
    assert response.status_code == 403
    assert response.json()['detail'] == NOT_AUTHORIZED


@pytest.mark.asyncio
async def test_category_members_authenticated_as_admin(client):
    # Arrange & Act
    jwt_token = admin_mock()
    response = client.get('admin_panel/actions/categories/members/17',
                          headers={"Authorization": f"Bearer {jwt_token}"})

    # Assert
    if response.status_code == 200:
        assert isinstance(response.json(), list)
    else:
        assert response.status_code == 404