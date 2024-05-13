from __future__ import annotations
from data.database import read_query, insert_query, update_query
from fastapi import HTTPException
from pydantic import Field
from models.models import Category


async def check_all_existing_categories(
    page: int = 1, size: int = 10, sort_by: str = None, search_query: str = None
):
    start = (page - 1) * size
    sql = 'SELECT * FROM category'
    if search_query:
        sql += f" WHERE name LIKE '%{search_query}%'"
    if sort_by:
        sql += f' ORDER BY {sort_by}'
    sql += f' LIMIT {size} OFFSET {start}'
    data = read_query(sql)
    if data:
        result = format_category_details(data)
        total_categories = len(result)
        return {
            "Total Categories": total_categories,
            "Page": page,
            "Size": size,
            "Categories": result
        }
    else:
        raise HTTPException(status_code=404, detail='There are currently no categories created!')



async def check_category_by_id(category_id: int = Field(..., gt=0)):
    data = read_query('SELECT * FROM category '
                      'WHERE category_id = %s', (category_id,))
    if not data:
        raise HTTPException(status_code=404, detail='There is no category with such ID')
    topics_data = read_query('SELECT * FROM topic WHERE category_id = %s', (category_id,))
    formatted_category_data = format_category_details(data)
    formatted_topics_data = format_topic_details(topics_data)
    formatted_category_data[0]["Topics"] = formatted_topics_data
    return formatted_category_data


async def check_category_by_name(category_name: str = Field(..., max_length=45)):
    data = read_query('SELECT * FROM category '
                      'WHERE title = %s', (category_name,))
    if any(data):
        return format_category_details(data)
    else:
        raise HTTPException(status_code=404, detail='There is no category with such Name')


async def create(category: Category):
    check_duplicates = read_query('SELECT * FROM category WHERE Title = %s', (category.title,))

    if any(check_duplicates):
        raise HTTPException(status_code=409, detail='A category with this name already exists')
    else:
        insert_query('INSERT INTO category(title) VALUES(%s)', (category.title,))
        await insert_all_users_inside(category.title)
        return f'Category with name {category.title} successfully created!'

async def insert_all_users_inside(category_name):
    users = read_query('SELECT user_id FROM users')
    category_id = read_query('SELECT category_id FROM category WHERE title = %s', (category_name,))
    for user in users:
        insert_query("INSERT INTO category_access (user_id,category_id, access_control) VALUES (%s, %s, %s)", (user[0], category_id[0][0], 2))

def check_if_reply_exists(reply_id: int = Field(..., gt=0)):
    sql = 'SELECT content FROM replies WHERE reply_id = %s'
    existing = read_query(sql, (reply_id,))
    return existing

async def delete_by_name(category_name: str = Field(..., max_length=45)):
    check_for_existing = read_query('SELECT * FROM category WHERE Title = %s', (category_name,))
    if not check_for_existing:
        raise HTTPException(status_code=404, detail='Category with such ID not found')

    category_id = read_query('SELECT category_id FROM category WHERE title = %s', (category_name,))
    topics = read_query('SELECT topic_id FROM topic WHERE category_id = %s', (category_id[0][0],))
    if topics:
        for topic in topics:
            delete_topic_by_id(topic[0])

    update_query('DELETE FROM category_access WHERE category_id = %s', (category_id[0][0],))
    update_query('DELETE FROM category WHERE title = %s', (category_name,))
    return f'Category with name {category_name} successfully deleted!'


def delete_topic_by_id(topic_id: int = Field(..., gt=0)):
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

def format_category_details(category_details_list):
    return [{
        'Category ID': category_detail[0],
        'Category Name': category_detail[1]
    } for category_detail in category_details_list]
