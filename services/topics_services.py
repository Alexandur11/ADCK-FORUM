from data.database import read_query, insert_query, update_query
from services.categories_services import check_category_by_id
from fastapi import HTTPException
from services.admin_services import get_user_by_id
from pydantic import Field


def checkout_topics(sort_by: str = None, search_query: str = None):
    sql = 'SELECT * FROM topic'
    if sort_by:
        sql += f' ORDER BY {sort_by}'
    if search_query:
        sql += f" WHERE name LIKE '%{search_query}%'"
    data = read_query(sql)
    if data:
        return format_topic_details(data)
    else:
        raise HTTPException(status_code=404, detail='There are currently no topics created!')


def check_topic_by_id(topic_id: int = Field(..., gt=0)):
    sql = 'SELECT * FROM topic WHERE topic_id = %s'
    data = read_query(sql, (topic_id,))
    replies_sql = 'SELECT * FROM replies WHERE topic_id = %s'
    replies_data = read_query(replies_sql, (topic_id,))
    if not data:
        raise HTTPException(status_code=404, detail='There is no topic with such ID!')
    formatted_topic_details = format_topic_details(data)
    formatted_replies_details = format_reply_details(replies_data)
    formatted_topic_details[0]["Replies"] = formatted_replies_details
    return formatted_topic_details


def check_topic_by_name(name_of_topic: str = Field(..., max_length=45)):
    sql = 'SELECT * FROM topic WHERE name LIKE %s'
    data = read_query(sql, (name_of_topic,))
    if data:
        return format_topic_details(data)
    else:
        raise HTTPException(status_code=404, detail='There is no topic with such name!')


def check_for_write_access(category_id: int = Field(None, gt=0),
                           user_id: int = Field(None, gt=0)):
    sql = "SELECT access_control FROM category_access WHERE category_id = %s AND user_id = %s"
    result = read_query(sql, (category_id, user_id))
    if result:
        access_level = result[0][0]
        return access_level == 2
    else:
        return False


async def create_topic(user_id: int = Field(gt=0), category_id: int = Field(gt=0),
                       name: str = Field(min_length=1)):
    if not get_user_by_id(user_id):
        raise HTTPException(status_code=404, detail='User not found!')
    if await check_category_by_id(category_id) is None:
        raise HTTPException(status_code=404, detail="Category not found!")
    if category_is_Closed(category_id)  == []:
        raise HTTPException(status_code=409, detail='Category is CLOSED!')
    if topic_exists(name):
        raise HTTPException(status_code=409, detail='A topic with this name already exists.')

    else:
        return create_new_topic(name, user_id, category_id)


def create_new_topic(topic_name, user_id, category_id):
    if not check_for_write_access(category_id, user_id):
        raise HTTPException(status_code=403, detail="You dont have write access to this category!")
    insert_query('INSERT INTO topic(name, users_id, category_id) VALUES (%s, %s, %s)',
                 (topic_name, user_id, category_id))
    return {'message': 'Topic created!'}


def check_if_user_is_creator(user_id: int, topic_id: int):
    sql = "SELECT * FROM topic WHERE topic_id = %s AND users_id = %s"
    execute = read_query(sql, (topic_id, user_id,))
    return execute


def check_if_reply_exists(reply_id: int = Field(..., gt=0)):
    sql = 'SELECT content FROM replies WHERE reply_id = %s'
    existing = read_query(sql, (reply_id,))
    return existing


def choose_best_reply(user_id: int = Field(gt=0), topic_id: int = Field(gt=0),
                      reply_id: int = Field(gt=0)):
    if not check_if_user_is_creator(user_id, topic_id):
        raise HTTPException(status_code=403, detail="You are not the creator of this topic!")
    if not check_if_reply_exists(reply_id):
        raise HTTPException(status_code=404, detail="Reply not found!")
    sql = "UPDATE topic SET best_reply = %s WHERE topic_id = %s"
    update_query(sql, (reply_id, topic_id))
    return {"message": "Reply pinned!"}


def category_is_Closed(category_id):
    return read_query('SELECT * FROM category WHERE category_id = %s AND is_open = %s', (category_id, 1))


def topic_exists(topic_name):
    return read_query('SELECT * FROM topic WHERE topic.name = %s', (topic_name,))


def delete_topic_by_id(topic_id: int = Field(..., gt=0)):
    if not check_topic_by_id(topic_id):
        raise HTTPException(status_code=404, detail="A topic with this ID does not exist.")
    sql_delete = 'DELETE FROM topic WHERE topic_id = %s'
    sql_delete_existing_replies = "DELETE FROM replies where topic_id = %s"
    update_query(sql_delete_existing_replies, (topic_id,))
    update_query(sql_delete, (topic_id,))
    return {'message': 'Topic deleted!'}


def format_topic_details(topic_details_list):
    formatted_details = []
    for topic_detail in topic_details_list:
        formatted_detail = {
            "Topic ID": topic_detail[0],
            "Category ID": topic_detail[1],
            "Topic name": topic_detail[2],
            "User ID": topic_detail[3],
            "Is open": "Yes" if topic_detail[4] else "No"
        }
        if topic_detail[5]:
            formatted_detail["Best reply"] = check_if_reply_exists(topic_detail[5])[0][0]
        formatted_details.append(formatted_detail)
    return formatted_details


def format_reply_details(reply_details_list):
    return [{
        "Reply ID": reply_detail[0],
        "Date posted": reply_detail[1],
        "Reply content": reply_detail[2],
        "Likes": reply_detail[3],
        "Dislikes": reply_detail[4],
        "User ID": reply_detail[5],
    } for reply_detail in reply_details_list]