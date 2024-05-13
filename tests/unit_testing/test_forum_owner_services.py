from services import forum_owner_services
from routers.forum_owner import *

from tests.unit_testing.mock_unit_users_data import *
import pytest


@pytest.mark.asyncio
async def test_create_admin_unauthenticated():
    with pytest.raises(HTTPException) as exc_info:
        await create_admin(None, 1)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == NOT_AUTHENTICATED

@pytest.mark.asyncio
async def test_create_admin_authenticated_as_user():
    user = user_mock()
    with pytest.raises(HTTPException) as exc_info:
        await create_admin(user, 1)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == NOT_AUTHORIZED

@pytest.mark.asyncio
async def test_demote_admin_unauthenticated():
    with pytest.raises(HTTPException) as exc_info:
        await demote_admin(None, 1)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == NOT_AUTHENTICATED

@pytest.mark.asyncio
async def test_demote_admin_authenticated_as_user():
    user = user_mock()
    with pytest.raises(HTTPException) as exc_info:
        await demote_admin(user, 1)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == NOT_AUTHORIZED

@pytest.mark.asyncio
async def test_delete_admin_unauthenticated():
    with pytest.raises(HTTPException) as exc_info:
        await delete_admin(None, 1)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == NOT_AUTHENTICATED

@pytest.mark.asyncio
async def test_delete_admin_authenticated_as_user():
    user = user_mock()
    with pytest.raises(HTTPException) as exc_info:
        await delete_admin(user, 1)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == NOT_AUTHORIZED

def test_promote_when_user_exists(mocker):
    data = list(mock_user_details_list[0])
    mocker.patch('services.forum_owner_services.read_query', mocker.MagicMock(return_value=data))
    mocker.patch('services.forum_owner_services.update_query')

    result = forum_owner_services.promote(1)

    assert result == {"message": ['User Promoted']}

def test_promote_when_user_does_not_exist(mocker):
    mocker.patch('services.forum_owner_services.read_query', mocker.MagicMock(return_value=[]))
    with pytest.raises(HTTPException) as exc_info:
        forum_owner_services.promote(1)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == f'This Account is already an Admin or Account with ID {1} does not exist'

def test_demote_when_user_exists(mocker):
    data = list(mock_user_details_list[0])
    mocker.patch('services.forum_owner_services.read_query', mocker.MagicMock(return_value=data))
    mocker.patch('services.forum_owner_services.update_query')

    result = forum_owner_services.demote(1)

    assert result == {"message": ['User Demoted']}

def test_demote_when_user_does_not_exist(mocker):
    mocker.patch('services.forum_owner_services.read_query', mocker.MagicMock(return_value=[]))
    with pytest.raises(HTTPException) as exc_info:
        forum_owner_services.demote(1)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == f'This Account is not an Admin or Account with ID {1} does not exist'

def test_delete_admin_account_when_exist(mocker):
    # Arrange
    data = list(mock_user_details_list[0])
    mocker.patch('services.forum_owner_services.read_query', mocker.MagicMock(return_value=data))
    mocker.patch('services.forum_owner_services.update_query')

    # Act
    result = delete_admin_account(1)

    # Assert
    assert result == {'message': ['User deleted successfully!']}


def test_delete_admin_account_when_does_not_exist(mocker):
    # Arrange
    mocker.patch('services.forum_owner_services.read_query', mocker.MagicMock(return_value=[]))

    with pytest.raises(HTTPException) as exc_info:
        forum_owner_services.delete_admin_account()

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == f'This Account is not an Admin or does not exist!'