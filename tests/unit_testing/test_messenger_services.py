import pytest

from services import messenger_services
from services.messenger_services import format_chat_details
from tests.unit_testing.mock_unit_users_data import *
from routers.messenger import *


@pytest.mark.asyncio
async def test_view_conversations_unauthenticated():
    with pytest.raises(HTTPException) as exc_info:
        await view_conversations(None)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_view_conversation_history_unauthenticated():
    with pytest.raises(HTTPException) as exc_info:
        await view_conversation_history(None, 1)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_new_chat_unauthenticated():
    with pytest.raises(HTTPException) as exc_info:
        await new_chat(None, 'Alex')

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_delete_conversation_unauthenticated():
    with pytest.raises(HTTPException) as exc_info:
        await delete_conversation(None, 1)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_insert_member_unauthenticated():
    with pytest.raises(HTTPException) as exc_info:
        await insert_members(None, 'Alex', 1)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_message_someone_unauthenticated():
    message = Message(conversation_id=1, text='Alo, da ?')
    with pytest.raises(HTTPException) as exc_info:
        await message_someone(None, message)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == NOT_AUTHENTICATED


@pytest.mark.asyncio
async def test_check_all_conversations_when_any_exist(mocker):
    data = CONVERSATIONS_DETAILS_MOCK
    expected = format_chat_details(data)
    mocker.patch('services.messenger_services.read_query', return_value=data)

    result = await messenger_services.check_all_conversations(user_id=1)

    assert result == ({'Total conversations': len(data)}, expected)


@pytest.mark.asyncio
async def test_check_all_conversations_when_none_exist(mocker):
    mocker.patch('services.messenger_services.read_query', return_value=[])

    with pytest.raises(HTTPException) as exc_info:
        await messenger_services.check_all_conversations(user_id=1)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == 'You are currently participating in 0 conversations!'


@pytest.mark.asyncio
async def test_conversation_history_when_any(mocker):
    data = MESSAGE_DETAILS_MOCK
    expected = format_chat_history(data)
    mocker.patch('services.messenger_services.read_query', return_value=data)

    result = await messenger_services.conversation_history(1)

    assert result == expected


@pytest.mark.asyncio
async def test_conversation_history_when_zero_exist(mocker):
    mocker.patch('services.messenger_services.read_query', return_value=[])

    with pytest.raises(HTTPException) as exc_info:
        await messenger_services.conversation_history(1)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == 'No messages in this conversation yet'


@pytest.mark.asyncio
async def test_delete_conversation_by_id_when_exists(mocker):
    data = CONVERSATIONS_DETAILS_MOCK
    mocker.patch('services.messenger_services.read_query', return_value=data)
    mocker.patch('services.messenger_services.update_query')

    result = await messenger_services.delete_conversation_by_id(1)

    assert result == f'Conversation with ID {1} was successfully deleted!'


@pytest.mark.asyncio
async def test_delete_conversation_by_id_when_does_not_exists(mocker):
    mocker.patch('services.messenger_services.read_query', return_value=[])
    with pytest.raises(HTTPException) as exc_info:
        await messenger_services.delete_conversation_by_id(1)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == f'No conversation with ID {1} was found!'


@pytest.mark.asyncio
async def test_room_when_desired_does_exist(mocker):
    room_name = f'{'username'}|{'desired_person'}'
    mocker.patch('services.messenger_services.find_user', return_value='desired_person')
    mocker.patch('services.messenger_services.read_query', return_value=room_name)
    result = await messenger_services.room('username', 'desired_person')

    assert result == """Write the logic which prompts the user the conversation tab 
        between him and the desired person
        """


@pytest.mark.asyncio
async def test_room_when_desired_person_does_exist(mocker):
    mocker.patch('services.messenger_services.find_user', return_value=True)
    mocker.patch('services.messenger_services.read_query', side_effect=[[], [(1,)]])
    mocker.patch('services.messenger_services.insert_query')
    result = await messenger_services.room('username', 'desired_person')
    assert result == (1)


@pytest.mark.asyncio
async def test_initial_members(mocker):
    mocker.patch('services.messenger_services.read_query', return_value=[[1]])
    mocker.patch('services.messenger_services.insert_query')
    result = await messenger_services.initial_members(1, 1, 1)

    assert result == 'Users successfully added to the chat.'


@pytest.mark.asyncio
async def test_add_another_member_when_user_exist(mocker):
    mocker.patch('services.messenger_services.read_query', return_value=[[1]])
    mocker.patch('services.messenger_services.update_query')
    result = await messenger_services.add_another_member('username', 1)

    assert result == f'Member with ID {1} was successfully added to conversation with ID {1}'


@pytest.mark.asyncio
async def test_your_message(mocker):
    mocker.patch('services.messenger_services.update_query')
    result = await messenger_services.your_message(1,
                                                   Message(conversation_id=1, text='hello'))

    assert result == 'Message successfully sent'
