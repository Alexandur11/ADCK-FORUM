from typing import Annotated

from fastapi import APIRouter, Depends
from services.login_services import get_current_user
from services.reply_services import add_reply, delete_reply, get_by_id, get_all, get_by_topic, like, dislike


reply_router = APIRouter(prefix='/replies')
user_dependency = Annotated[dict, Depends(get_current_user)]


@reply_router.post(path='/new', status_code=201)
def add_new_reply(user: user_dependency, topic_id: int, content: str):
    """
    This method takes a user ID, a topic ID, and the content (text) of the reply and adds it to the topic's replies
    """
    user_id = user.get("id")
    return add_reply(user_id, topic_id, content)


@reply_router.delete(path='', status_code=204)
def delete_reply_by_id(user: user_dependency, reply_id: int):
    """
    This method takes in a reply ID and deletes it
    """
    return delete_reply(reply_id)


@reply_router.get(path='/all', status_code=200)
def get_all_replies(user: user_dependency):
    """
    This method gives info about all the existing replies regardless of topic
    """
    return get_all()


@reply_router.get(path='/{reply_id}', status_code=200)
def get_reply_by_id(user: user_dependency, reply_id: int):
    """
    This method takes a reply ID and gives info about the reply it belongs to
    """
    return get_by_id(reply_id)


@reply_router.get(path='/all/{topic_id}', status_code=200)
def get_by_topic_id(user: user_dependency, topic_id: int):
    """
    This method takes a topic ID and gives info about all replies regarding this topic
    """
    return get_by_topic(topic_id)


@reply_router.put(path='/like/{reply_id}', status_code=200)
def like_reply(user: user_dependency, reply_id: int):
    """
    This method servers as an endpoint for a 'LIKE' button
    """
    user_id = user.get("id")
    return like(user_id, reply_id)


@reply_router.put(path='/dislike/{reply_id}', status_code=200)
def dislike_reply(user: user_dependency, reply_id: int):
    """
    This method servers as an endpoint for a 'DISLIKE' button
    """
    user_id = user.get("id")
    return dislike(user_id, reply_id)
