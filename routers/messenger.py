from typing import Annotated

from services.login_services import get_current_user
from services.messenger_services import (check_all_conversations, conversation_history,
                                         initial_members, delete_conversation_by_id, add_another_member, your_message,
                                         room)
from fastapi import APIRouter, Depends, HTTPException
from models.models import Message

messenger_router = APIRouter(prefix='/messenger')
user_dependency = Annotated[dict, Depends(get_current_user)]

NOT_AUTHORIZED = "Not authorized"
NOT_AUTHENTICATED = "Not authenticated"


@messenger_router.get('', status_code=200)
async def view_conversations(user: user_dependency):
    """
    This method returns all conversations in which the user is participating.
    """
    if user is None:
        raise HTTPException(status_code=401, detail=NOT_AUTHENTICATED)
    return await check_all_conversations(user.get("id"))


@messenger_router.get('/{conversation_id}', status_code=200)
async def view_conversation_history(user: user_dependency, conversation_id: int):
    """
    This method returns the conversation with the desired ID. If it exists.
    """
    if user is None:
        raise HTTPException(status_code=401, detail=NOT_AUTHENTICATED)
    return await conversation_history(conversation_id)


@messenger_router.post('/new', status_code=201)
async def new_chat(user: user_dependency, desired_person: str, group_name=None):
    """
    This method created a conversation, allows a name to be select
    for the chat and adds the two members into a room together.
    """
    if user is None:
        raise HTTPException(status_code=401, detail=NOT_AUTHENTICATED)

    room_id = await room(user.get("username"), desired_person, group_name)
    return await initial_members(room_id, user.get("id"), desired_person)


@messenger_router.delete('/delete', status_code=204)
async def delete_conversation(user: user_dependency, conversation_id: int):
    """
    This method deleted the conversation with the desired ID.
    """
    if user is None:
        raise HTTPException(status_code=401, detail=NOT_AUTHENTICATED)
    return await delete_conversation_by_id(conversation_id)


@messenger_router.put('/add_members', status_code=200)
async def insert_members(user: user_dependency, username: str, conversation_id: int):
    """
    This method inserts a new member
    inside the desired conversation if both objects exist.
    """
    if user is None:
        raise HTTPException(status_code=401, detail=NOT_AUTHENTICATED)
    return await add_another_member(username, conversation_id)


@messenger_router.post('/message/new', status_code=201)
async def message_someone(user: user_dependency, message: Message):
    """
    This method sends a message using the Message model.
    """
    if user is None:
        raise HTTPException(status_code=401, detail=NOT_AUTHENTICATED)
    return await your_message(user.get("id"), message)
