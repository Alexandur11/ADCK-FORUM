from typing import Annotated
from fastapi import APIRouter, Depends, Query
from services.login_services import get_current_user
from services.topics_services import (create_topic, checkout_topics,
                                      check_topic_by_id, check_topic_by_name, delete_topic_by_id,
                                      choose_best_reply)


topics_router = APIRouter(prefix='/topics')
user_dependency = Annotated[dict, Depends(get_current_user)]


@topics_router.get('', status_code=200)
async def check_all_topics(user: user_dependency,
                           sort_by: str = Query(None, description="Column to sort by", alias="sort",
                                                examples=["name", "users_id", "category_id",
                                                          "is_open"]),
                           search_query: str = Query(None, description="Search by name"),
                           page: int = Query(1, ge=1),
                           size: int = Query(10, ge=1, le=100)):
    """
    This method displays info about all existing topics. You can search and sort by different parameters
    """
    topics = checkout_topics(sort_by=sort_by, search_query=search_query)
    total_topics = len(topics)
    start = (page - 1) * size
    end = min(start + size, total_topics)
    paginated_topics = topics[start:end]
    return {
        "Topics": paginated_topics,
        "Total Topics": total_topics,
        "Page": page,
        "Size": size
    }


@topics_router.get('/{topic_id}', status_code=200)
async def view_topic(user: user_dependency, topic_id: int):
    """
    This method takes in the ID of the desired topic and displays info about it.
    """
    return check_topic_by_id(topic_id)


@topics_router.get('/name_search/{topic_name}', status_code=200)
async def get_topic_by_name(user: user_dependency, topic_name: str):
    """
    This method takes in the name of the desired topic and displays info about it.
    """
    return check_topic_by_name(topic_name)


@topics_router.post('/new', status_code=201)
async def new_topic(user: user_dependency, category_id: int, name: str):
    """
    This method takes in the
    topic title, the ID of the user and the ID of the category,
    then creates a topic within that category.
    """
    user_id = user.get("id")
    return await create_topic(user_id, category_id, name)


@topics_router.delete('', status_code=204)
async def delete_topic(user: user_dependency, topic_id: int):
    """
    This method takes in the ID of the topic and deletes it.
    """
    return delete_topic_by_id(topic_id)


@topics_router.post("/best_reply/{topic_id}")
async def pin_best_reply(user: user_dependency, topic_id: int, reply_id: int):
    """
    This method allows the creator of the topic to pin the best reply to it
    """
    user_id = user.get("id")
    return choose_best_reply(user_id, topic_id, reply_id)
