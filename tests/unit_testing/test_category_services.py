from services import categories_services
from tests.unit_testing.mock_unit_users_data import *
import pytest


from routers.categories import *


@pytest.mark.asyncio
async def test_check_all_categories_unauthenticated():
    with pytest.raises(HTTPException) as exc_info:
        await check_all_categories(None)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_check_all_categories_authenticated_as_user():
    user = user_mock()
    with pytest.raises(HTTPException) as exc_info:
        await check_all_categories(user)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == NOT_AUTHORIZED


@pytest.mark.asyncio
async def test_view_category_unauthenticated():
    with pytest.raises(HTTPException) as exc_info:
        await view_category(None, 1)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_get_by_name_unauthenticated():
    with pytest.raises(HTTPException) as exc_info:
        await get_by_name(None, "Alex")

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_get_by_name_authenticated_as_user():
    user = user_mock()
    with pytest.raises(HTTPException) as exc_info:
        await get_by_name(user, "Alex")

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == NOT_AUTHORIZED


@pytest.mark.asyncio
async def test_new_category_unauthenticated():
    category = Category(title="Alex")
    with pytest.raises(HTTPException) as exc_info:
        await new_category(None, category)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_new_category_authenticated_as_user():
    category = Category(title="Alex")
    user = user_mock()
    with pytest.raises(HTTPException) as exc_info:
        await new_category(user, category)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == NOT_AUTHORIZED


@pytest.mark.asyncio
async def test_delete_category_unauthenticated():
    with pytest.raises(HTTPException) as exc_info:
        await delete_category(None, 'Alex')

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_delete_category_authenticated_as_user():
    user = user_mock()
    with pytest.raises(HTTPException) as exc_info:
        await delete_category(user, 'Alex')

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == NOT_AUTHORIZED


@pytest.mark.asyncio
async def check_category_by_id_when_exists(mocker):
    pass


@pytest.mark.asyncio
async def test_check_category_by_id_when_does_not_exists(mocker):
    mocker.patch('services.categories_services.read_query', mocker.MagicMock(return_value=[]))
    with pytest.raises(HTTPException) as exc_info:
        await categories_services.check_category_by_id(1)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == 'There is no category with such ID'


@pytest.mark.asyncio
async def test_check_category_by_name_when_exists(mocker):
    data = [(1, 'Category_name')]
    expected = mock_format_category_details(data)
    mocker.patch('services.categories_services.read_query', mocker.MagicMock(return_value=data))
    result = await categories_services.check_category_by_name('Category_name')

    assert result == expected


@pytest.mark.asyncio
async def test_check_category_by_name_when_does_not_exists(mocker):
    mocker.patch('services.categories_services.read_query', mocker.MagicMock(return_value=[]))
    with pytest.raises(HTTPException) as exc_info:
        await categories_services.check_category_by_name('Category_name')

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == 'There is no category with such Name'



@pytest.mark.asyncio
async def test_create_raise_error_for_existence(mocker):
    data = [(1, 'Title')]
    mocker.patch('services.categories_services.read_query', mocker.MagicMock(return_value=data))

    with pytest.raises(HTTPException) as exc_info:
        await categories_services.create(Category(title='Title'))

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == 'A category with this name already exists'


@pytest.mark.asyncio
async def test_create_when_name_available(mocker):
    mocker.patch('services.categories_services.read_query', mocker.MagicMock(return_value=[]))
    mocker.patch('services.categories_services.insert_query')

    result = await categories_services.create(Category(title='Title'))
    expected = 'Category with name Title successfully created!'''

    assert result == expected


@pytest.mark.asyncio
async def test_delete_category_by_name_when_does_not_exists(mocker):
    mocker.patch('services.categories_services.read_query', mocker.MagicMock(return_value=[]))
    mocker.patch('services.categories_services.update_query')

    with pytest.raises(HTTPException) as exc_info:
        await categories_services.delete_by_name('Title')

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == 'Category with such ID not found'


@pytest.mark.asyncio
async def test_delete_category_by_name_when_exists(mocker):
    data = [(1, 'Title')]
    mocker.patch('services.categories_services.read_query', mocker.MagicMock(return_value=data))
    mocker.patch('services.categories_services.update_query')
    expected = 'Category with name Title successfully deleted!'

    result = await categories_services.delete_by_name('Title')

    assert result == expected
