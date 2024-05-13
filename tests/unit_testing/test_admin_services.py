from services import admin_services
from routers.admin import *
from tests.unit_testing.mock_unit_users_data import *
import pytest


@pytest.mark.asyncio
async def test_get_all_when_unauthenticated():
    with pytest.raises(HTTPException) as exc_info:
        await get_all(None)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_get_all_when_authenticated_as_user():
    user = user_mock()

    with pytest.raises(HTTPException) as exc_info:
        await get_all(user)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == NOT_AUTHORIZED


@pytest.mark.asyncio
async def test_search_by_id_when_unauthenticated():
    with pytest.raises(HTTPException) as exc_info:
        await search_user_by_id(None, 1)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_search_by_id_when_authenticated_as_user():
    user = user_mock()
    with pytest.raises(HTTPException) as exc_info:
        await search_user_by_id(user, 1)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == NOT_AUTHORIZED


@pytest.mark.asyncio
async def test_search_by_username_when_unauthenticated():
    with pytest.raises(HTTPException) as exc_info:
        await search_user_by_username(None, "Dwight")

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_search_by_username_when_authenticated_as_user():
    user = user_mock()
    with pytest.raises(HTTPException) as exc_info:
        await search_user_by_username(user, "Dwight")

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == NOT_AUTHORIZED


@pytest.mark.asyncio
async def test_is_logged_unauthenticated():
    with pytest.raises(HTTPException) as exc_info:
        await is_logged(None, 1)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_is_logged_authenticated_as_user():
    user = user_mock()
    with pytest.raises(HTTPException) as exc_info:
        await is_logged(user, 1)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == NOT_AUTHORIZED


@pytest.mark.asyncio
async def test_all_logged_unauthenticated():
    with pytest.raises(HTTPException) as exc_info:
        await all_logged(None)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_all_logged_authenticated_as_user():
    user = user_mock()
    with pytest.raises(HTTPException) as exc_info:
        await all_logged(user)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == NOT_AUTHORIZED


@pytest.mark.asyncio
async def test_delete_user_unauthenticated():
    with pytest.raises(HTTPException) as exc_info:
        await delete_user(None, 1)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_delete_user_authenticated_as_user():
    user = user_mock()
    with pytest.raises(HTTPException) as exc_info:
        await delete_user(user, 1)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == NOT_AUTHORIZED


@pytest.mark.asyncio
async def test_lock_topic_by_id_unauthenticated():
    with pytest.raises(HTTPException) as exc_info:
        await lock_topic_by_id(None, 1)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_lock_topic_by_id_authenticated_as_user():
    user = user_mock()
    with pytest.raises(HTTPException) as exc_info:
        await lock_topic_by_id(user, 1)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == NOT_AUTHORIZED


@pytest.mark.asyncio
async def test_unlock_topic_by_id_unauthenticated():
    with pytest.raises(HTTPException) as exc_info:
        await unlock_topic_by_id(None, 1)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_unlock_topic_by_id_authenticated_as_user():
    user = user_mock()
    with pytest.raises(HTTPException) as exc_info:
        await unlock_topic_by_id(user, 1)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == NOT_AUTHORIZED


@pytest.mark.asyncio
async def test_lock_category_by_id_unauthenticated():
    with pytest.raises(HTTPException) as exc_info:
        await lock_category_by_id(None, 1)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_lock_category_by_id_authenticated_as_user():
    user = user_mock()
    with pytest.raises(HTTPException) as exc_info:
        await lock_category_by_id(user, 1)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == NOT_AUTHORIZED


@pytest.mark.asyncio
async def test_unlock_category_by_id_unauthenticated():
    with pytest.raises(HTTPException) as exc_info:
        await unlock_category_by_id(None, 1)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_unlock_category_by_id_authenticated_as_user():
    user = user_mock()
    with pytest.raises(HTTPException) as exc_info:
        await unlock_category_by_id(user, 1)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == NOT_AUTHORIZED


@pytest.mark.asyncio
async def test_ban_user_by_id_unauthenticated():
    with pytest.raises(HTTPException) as exc_info:
        await ban_user_by_id(None, 1)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_ban_user_by_id_authenticated_as_user():
    user = user_mock()
    with pytest.raises(HTTPException) as exc_info:
        await ban_user_by_id(user, 1)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == NOT_AUTHORIZED


@pytest.mark.asyncio
async def test_give_write_unauthenticated():
    write = write_access_mock()
    with pytest.raises(HTTPException) as exc_info:
        await give_write(None, write)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_give_write_authenticated_as_user():
    write = write_access_mock()
    user = user_mock()
    with pytest.raises(HTTPException) as exc_info:
        await give_write(user, write)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == NOT_AUTHORIZED


@pytest.mark.asyncio
async def test_give_read_unauthenticated():
    read = read_access_mock()
    with pytest.raises(HTTPException) as exc_info:
        await give_read(None, read)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_give_read_authenticated_as_user():
    read = read_access_mock()
    user = user_mock()
    with pytest.raises(HTTPException) as exc_info:
        await give_read(user, read)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == NOT_AUTHORIZED


@pytest.mark.asyncio
async def test_revoke_unauthenticated():
    revoke_object = revoke_access_mock()
    with pytest.raises(HTTPException) as exc_info:
        await revoke(None, revoke_object)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_revoke_authenticated_as_user():
    revoke_object = revoke_access_mock()
    user = user_mock()
    with pytest.raises(HTTPException) as exc_info:
        await revoke(user, revoke_object)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == NOT_AUTHORIZED


@pytest.mark.asyncio
async def test_category_members_unauthenticated():
    with pytest.raises(HTTPException) as exc_info:
        await category_members(None, 1)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_category_members_authenticated_as_user():
    user = user_mock()
    with pytest.raises(HTTPException) as exc_info:
        await category_members(user, 1)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == NOT_AUTHORIZED


def test_get_all_users_when_any(mocker):
    # Arrange
    data = mock_user_details_list
    expected = mock_format_user_details(data)

    # Act & Assert
    mocker.patch('services.admin_services.read_query', mocker.MagicMock(return_value=data))
    data = admin_services.get_all_users()
    assert data == ({'Total users': len(data)}, expected)


def test_get_all_users_raises_error_when_no_users(mocker):
    # Arrange
    mocker.patch('services.admin_services.read_query', mocker.MagicMock(return_value=[]))

    # Act and Assert
    with pytest.raises(HTTPException) as exc_info:
        admin_services.get_all_users()

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == 'There are currently no users registered!'


def test_get_all_users_by_id_when_any(mocker):
    # Arrange
    user_details = mock_user_details_list[0]
    data = [user_details]
    expected = mock_format_user_details(data)

    # Act & Assert
    mocker.patch('services.admin_services.read_query', mocker.MagicMock(return_value=data))
    data = admin_services.get_user_by_id(user_id=1)

    # Assert the result
    assert data == expected


def test_get_user_by_id_raises_error_when_no_user(mocker):
    # Arrange
    mocker.patch('services.admin_services.read_query', mocker.MagicMock(return_value=[]))

    # Act and Assert
    with pytest.raises(HTTPException) as exc_info:
        admin_services.get_user_by_id()

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == USER_NOT_FOUND


def test_get_all_users_by_username_when_any(mocker):
    # Arrange
    user_details = mock_user_details_list[0]
    data = [user_details]
    expected = mock_format_user_details(data)

    # Act & Assert
    mocker.patch('services.admin_services.read_query', mocker.MagicMock(return_value=data))
    data = admin_services.get_user_by_username(username='Alexandur')

    # Assert the result
    assert data == expected


def test_get_user_by_username_raises_error_when_no_user(mocker):
    # Arrange
    mocker.patch('services.admin_services.read_query', mocker.MagicMock(return_value=[]))

    # Act and Assert
    with pytest.raises(HTTPException) as exc_info:
        admin_services.get_user_by_username()

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == USER_NOT_FOUND


def test_check_if_user_is_logged_when_False():
    # Arrange & Act
    data = check_if_user_is_logged(1)
    expected = False, {'message': 'User is not logged in!'}

    # Assert
    assert data == expected


def test_check_all_logged_when_None_raise_error():
    with pytest.raises(HTTPException) as exc_info:
        admin_services.check_all_logged()

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == 'Currently there are no users logged in.'


def test_delete_user_by_id_when_any(mocker):
    # Arrange
    data = list(mock_user_details_list[0])
    mocker.patch('services.admin_services.read_query', mocker.MagicMock(return_value=data))
    mocker.patch('services.admin_services.update_query')

    # Act
    result = delete_user_by_id(1)

    # Assert
    assert result == {'message': ['User deleted successfully!']}


def test_delete_user_by_id_raise_error_when_None(mocker):
    # Arrange
    data = []
    mocker.patch('services.admin_services.read_query', mocker.MagicMock(return_value=data))

    with pytest.raises(HTTPException) as exc_info:
        admin_services.delete_user_by_id()

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == USER_NOT_FOUND


def test_lock_category_by_id_when_any(mocker):
    data = OPEN_CATEGORY_MOCK
    expected = {'message': f"Category with ID {1} successfully locked."}
    mocker.patch('services.admin_services.update_query')
    mocker.patch('services.admin_services.read_query', mocker.MagicMock(return_value=data))
    data = admin_services.lock_category(category_id=1)
    assert data == expected


def test_lock_category_by_id_when_None(mocker):
    mocker.patch('services.admin_services.read_query', mocker.MagicMock(return_value=[]))
    with pytest.raises(HTTPException) as exc_info:
        admin_services.lock_category()

    assert exc_info.value.status_code == 404


def test_unlock_category_by_id_when_any(mocker):
    data = CLOSED_CATEGORY_MOCK
    expected = {"message": f"Category with ID {1} successfully unlocked."}
    mocker.patch('services.admin_services.update_query')
    mocker.patch('services.admin_services.read_query', mocker.MagicMock(return_value=data))
    data = admin_services.unlock_category(category_id=1)
    assert data == expected


def test_unlock_category_by_id_when_None(mocker):
    mocker.patch('services.admin_services.read_query', mocker.MagicMock(return_value=[]))
    with pytest.raises(HTTPException) as exc_info:
        admin_services.unlock_category()

    assert exc_info.value.status_code == 404


def test_lock_topic_by_id_when_any(mocker):
    data = OPEN_TOPIC_MOCK
    expected = {"message": f"Topic with ID {1} successfully locked."}
    mocker.patch('services.admin_services.update_query')
    mocker.patch('services.admin_services.read_query', mocker.MagicMock(return_value=data))
    data = admin_services.lock_topic(topic_id=1)
    assert data == expected


def test_lock_topic_by_id_when_None(mocker):
    mocker.patch('services.admin_services.read_query', mocker.MagicMock(return_value=[]))
    with pytest.raises(HTTPException) as exc_info:
        admin_services.lock_topic()

    assert exc_info.value.status_code == 404


def test_unlock_topic_by_id_when_any(mocker):
    data = CLOSED_TOPIC_MOCK
    expected = {"message": f"Topic with ID {1} successfully unlocked."}
    mocker.patch('services.admin_services.update_query')
    mocker.patch('services.admin_services.read_query', mocker.MagicMock(return_value=data))
    data = admin_services.unlock_topic(topic_id=1)
    assert data == expected


def test_unlock_topic_by_id_when_None(mocker):
    mocker.patch('services.admin_services.read_query', mocker.MagicMock(return_value=[]))
    with pytest.raises(HTTPException) as exc_info:
        admin_services.unlock_topic()

    assert exc_info.value.status_code == 404


def test_view_users_when_any(mocker):
    data = mock_user_details_list
    expected = mock_format_user_details(data)
    mocker.patch('services.admin_services.read_query', mocker.MagicMock(return_value=data))
    assert admin_services.view_users() == expected


def test_view_users_when_None(mocker):
    expected = "There are currently 0 users"
    mocker.patch('services.admin_services.read_query', mocker.MagicMock(return_value=[]))
    assert admin_services.view_users() == expected


def test_write_access_when_user_has_read(mocker):
    mock_data = AccessControl(user_id=1, category_id=1)
    mocker.patch('services.admin_services.read_query', mocker.MagicMock(return_value=mock_data))
    mocker.patch('services.admin_services.update_query')
    mocker.patch('services.admin_services.insert_query')

    result = admin_services.write_access(mock_data)

    # Assert the result
    assert result == {"message": ['Access updated']}


def test_write_access_when_user_has_no_rights(mocker):
    mock_data = AccessControl(user_id=1, category_id=1)
    mocker.patch('services.admin_services.read_query', mocker.MagicMock(return_value=[]))
    mocker.patch('services.admin_services.update_query')
    mocker.patch('services.admin_services.insert_query')

    result = admin_services.write_access(mock_data)

    # Assert the result
    assert result == {"message":
                          [f'Access was set to WRITE to User with ID{1} for Category with ID {1}!']}


def test_read_access_when_user_has_write(mocker):
    mock_data = AccessControl(user_id=1, category_id=1)
    mocker.patch('services.admin_services.read_query', mocker.MagicMock(return_value=mock_data))
    mocker.patch('services.admin_services.update_query')
    mocker.patch('services.admin_services.insert_query')

    result = admin_services.read_access(mock_data)

    # Assert the result
    assert result == {"message": ['Access updated']}


def test_read_access_when_user_has_no_rights(mocker):
    mock_data = AccessControl(user_id=1, category_id=1)
    mocker.patch('services.admin_services.read_query', mocker.MagicMock(return_value=[]))
    mocker.patch('services.admin_services.update_query')
    mocker.patch('services.admin_services.insert_query')

    result = admin_services.read_access(mock_data)

    # Assert the result
    assert result == f'Read access was given to User with ID{1} for Category with ID {1}!'


def test_revoke_access_when_user_exists(mocker):
    mock_data = AccessControl(user_id=1, category_id=1)
    mocker.patch('services.admin_services.read_query', mocker.MagicMock(return_value=mock_data))
    mocker.patch('services.admin_services.update_query')

    result = admin_services.revoke_access(mock_data)

    assert result == {"message":
                          [f'Access to category with ID {1} for user with ID {1} was revoked!']}


def test_revoke_access_when_user_does_not_exist(mocker):
    mock_data = AccessControl(user_id=1, category_id=1)
    mocker.patch('services.admin_services.read_query', mocker.MagicMock(return_value=[]))
    with pytest.raises(HTTPException) as exc_info:
        admin_services.revoke_access(mock_data)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == USER_NOT_FOUND
