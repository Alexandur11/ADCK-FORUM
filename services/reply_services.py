from fastapi import HTTPException
from pydantic import Field
from data.database import read_query, insert_query, update_query
from services.topics_services import check_topic_by_id


TOTAL_REPLIES = "Total replies"


def get_all():
    sql = 'SELECT * FROM replies'
    existing = read_query(sql)
    if existing:
        result = format_reply_details(existing)
        return {TOTAL_REPLIES: len(existing)}, result
    else:
        raise HTTPException(status_code=404, detail='No replies to any topics found!')


def get_by_id(reply_id: int = Field(..., gt=0)):
    sql = 'SELECT * FROM replies WHERE reply_id = %s'
    existing = read_query(sql, (reply_id,))
    if existing:
        result = format_reply_details(existing)
        return {TOTAL_REPLIES: len(existing)}, result
    else:
        raise HTTPException(status_code=404, detail='Reply not found!')


def add_reply(user_id: int = Field(gt=0), topic_id: int = Field(gt=0), content: str = Field(min_length=1)):
    if not check_topic_by_id(topic_id):
        raise HTTPException(status_code=404, detail="Topic not found!")
    if not check_if_topic_is_open(topic_id):
        raise HTTPException(status_code=403, detail="Topic is currently locked!")
    sql = 'INSERT INTO replies (users_id, topic_id, content, date_posted) VALUES (%s, %s, %s, NOW())'
    insert_query(sql, (user_id, topic_id, content))
    return {'message': 'Reply added to topic!'}


def check_if_topic_is_open(topic_id: int = (Field(gt=0))):
    sql = "SELECT * FROM topic WHERE topic_id = %s AND is_open = 1"
    state = read_query(sql, (topic_id, ))
    return state


def delete_reply(reply_id: int = Field(..., gt=0)):
    existing = get_by_id(reply_id)
    if existing:
        sql = 'DELETE FROM replies WHERE reply_id = %s'
        update_query(sql, (reply_id,))
        return {'message': 'Reply deleted!'}
    else:
        raise HTTPException(status_code=404, detail='Reply not found!')


def get_by_topic(topic_id: int = Field(..., gt=0)):
    existing = check_topic_by_id(topic_id)
    if existing:
        sql = 'SELECT * FROM replies WHERE topic_id = %s'
        data = read_query(sql, (topic_id,))
        if data:
            result = format_reply_details(data)
            return {TOTAL_REPLIES: len(data)}, result
        else:
            raise HTTPException(status_code=404, detail='No replies found!')
    else:
        raise HTTPException(status_code=404, detail='Topic not found!')


def format_reply_details(reply_details_list):
    return [{
        "Reply ID": reply_detail[0],
        "Date posted": reply_detail[1],
        "Reply content": reply_detail[2],
        "Likes": reply_detail[3],
        "Dislikes": reply_detail[4],
        "User ID": reply_detail[5],
        "Topic ID": reply_detail[6]
    } for reply_detail in reply_details_list]


def check_for_like(user_id: int = Field(gt=0), reply_id: int = Field(gt=0)):
    like_reply = "like"
    like_sql = "SELECT * FROM likes_dislikes WHERE user_id = %s AND type = %s AND reply_id = %s"
    execute = read_query(like_sql, (user_id, like_reply, reply_id))
    return execute


def check_for_dislike(user_id: int = Field(gt=0), reply_id: int = Field(gt=0)):
    dislike_reply = "dislike"
    like_sql = "SELECT * FROM likes_dislikes WHERE user_id = %s AND type = %s AND reply_id = %s"
    execute = read_query(like_sql, (user_id, dislike_reply, reply_id))
    return execute


def like(user_id: int = Field(gt=0), reply_id: int = Field(...,gt=0)):
    like_reply = "like"
    if not check_for_like(user_id, reply_id):
        sql_reply = "UPDATE replies SET likes = likes + 1 WHERE reply_id = %s"
        update_query(sql_reply, (reply_id,))
        sql_like = "INSERT INTO likes_dislikes (user_id, reply_id, type) VALUES (%s, %s, %s)"
        insert_query(sql_like, (user_id, reply_id, like_reply))
        return {"message": "You liked this reply!"}
    else:
        sql_reply = "UPDATE replies SET likes = likes - 1 WHERE reply_id = %s"
        update_query(sql_reply, (reply_id,))
        sql_remove_like = ("DELETE FROM likes_dislikes WHERE user_id = %s AND "
                           "reply_id = %s AND type = %s")
        update_query(sql_remove_like, (user_id, reply_id, like_reply))
        return {"message": "You unliked this reply!"}


def dislike(user_id: int = Field(..., gt=0), reply_id: int = Field(...,gt=0)):
    dislike_reply = "dislike"
    if not check_for_dislike(user_id, reply_id):
        sql_reply = "UPDATE replies SET dislikes = dislikes + 1 WHERE reply_id = %s"
        update_query(sql_reply, (reply_id,))
        sql_like = "INSERT INTO likes_dislikes (user_id, reply_id, type) VALUES (%s, %s, %s)"
        insert_query(sql_like, (user_id, reply_id, dislike_reply))
        return {"message": "You disliked this reply!"}
    else:
        sql_reply = "UPDATE replies SET dislikes = dislikes - 1 WHERE reply_id = %s"
        update_query(sql_reply, (reply_id,))
        sql_remove_dislike = ("DELETE FROM likes_dislikes WHERE user_id = %s AND "
                              "reply_id = %s AND type = %s")
        update_query(sql_remove_dislike, (user_id, reply_id, dislike_reply))
        return {"message": "You removed your dislike for this reply!"}
