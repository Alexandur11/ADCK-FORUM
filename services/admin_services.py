from data.database import read_query, update_query, insert_query
from fastapi import HTTPException
from pydantic import Field

from models.models import AccessControl

logged_in_users = {}

USER_NOT_FOUND = 'User not found!'
IS_ADMIN = 'Is admin'


def get_all_users():
    data = read_query('SELECT * FROM users')
    if data:
        result = format_user_details(data)
        return {'Total users': len(data)}, result
    else:
        raise HTTPException(status_code=404, detail='There are currently no users registered!')

def get_user_by_id(user_id: int = Field(..., gt=0)):
    sql = 'SELECT * FROM users WHERE user_id = %s'
    data = read_query(sql, (user_id,))
    if data:
        return format_user_details(data)
    else:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND)


def get_user_by_username(username: str = Field(..., max_length=45)):
    sql = 'SELECT * FROM users WHERE BINARY username = %s'
    data = read_query(sql, (username,))
    if data:
        return format_user_details(data)
    else:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND)


def get_users_by_first_name(name: str = Field(..., max_length=45)):
    sql = 'SELECT * FROM users WHERE firstname LIKE = %s'
    data = read_query(sql, (name,))
    if data:
        return format_user_details(data)
    else:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND)


def check_if_user_is_logged(user_id: int = Field(..., gt=0)):
    if str(user_id) in logged_in_users:
        logged_in = True
        return logged_in, {'message': 'User is logged in.'}
    else:
        logged_in = False
        return logged_in, {'message': 'User is not logged in!'}


def check_all_logged():
    data = []
    for user_id, user_info in logged_in_users.items():
        data.append({'User ID': user_id, 'Username': user_info['Username']})
    if data:
        return {'Total users logged in': len(data)}, data
    else:
        raise HTTPException(status_code=404, detail='Currently there are no users logged in.')


def delete_user_by_id(user_id: int = Field(..., gt=0)):
    user_to_delete = read_query('SELECT * FROM users WHERE user_id = %s', (user_id,))
    if user_to_delete:
        sql = (
            f"UPDATE users "
            f"SET username = 'Default{user_id}', "
            f"password = 'NULL', "
            f"firstname = NULL, "
            f"lastname = NULL, "
            f"email = NULL, "
            f"birth_date = NULL "
            f"WHERE user_id = %s")
        update_query(sql, (user_id,))
        return {'message': ['User deleted successfully!']}
    else:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND)


def lock_category(category_id: int = Field(..., gt=0)):
    data = read_query('SELECT * FROM category WHERE category_id = %s  AND is_open = %s', (category_id, 1))

    if any(data):
        update_query(f'UPDATE category SET is_open = {0} WHERE category_id = {category_id}')
        return {'message': f"Category with ID {category_id} successfully locked."}
    else:
        raise HTTPException(status_code=404,
                            detail=f'Category with ID {category_id} is either locked or does not exist anymore!')


def unlock_category(category_id: int = Field(..., gt=0)):
    data = read_query('SELECT * FROM category WHERE category_id = %s AND is_open = %s', (category_id, 0))

    if any(data):
        update_query(f'UPDATE category SET is_open = {1} WHERE category_id = {category_id}')
        return {"message" :f"Category with ID {category_id} successfully unlocked."}
    else:
        raise HTTPException(status_code=404,
                            detail=f'Category with ID {category_id} is either unlocked or dos not exist anymore!')


def lock_topic(topic_id: int = Field(..., gt=0)):
    data = read_query('SELECT * FROM topic WHERE topic_id = %s AND is_open = %s', (topic_id, 1))

    if any(data):
        update_query(f'UPDATE topic SET is_open = {0} WHERE topic_id = {topic_id}')
        return {"message" : f"Topic with ID {topic_id} successfully locked."}
    else:
        raise HTTPException(status_code=404,
                            detail=f'Topic with ID {topic_id} is either already locked or does not exist anymore!')


def unlock_topic(topic_id: int = Field(..., gt=0)):
    data = read_query('SELECT * FROM topic WHERE topic_id = %s AND is_open = %s', (topic_id, 0))
    if any(data):
        update_query(f'UPDATE topic SET is_open = {1} WHERE topic_id = {topic_id}')
        return {"message": f"Topic with ID {topic_id} successfully unlocked."}
    else:
        raise HTTPException(status_code=404,
                            detail=f'Topic with ID {topic_id} is either already unlocked or does not exist anymore!')


def view_users():
    data = read_query('SELECT * FROM users')
    if any(data):
        return format_user_details(data)
    else:
        return "There are currently 0 users"


def write_access(accesscontrol: AccessControl):
    data = read_query('SELECT * FROM category_access WHERE user_id = %s AND category_id = %s',
                      (accesscontrol.user_id, accesscontrol.category_id))

    if any(data):
        update_query(
            f'UPDATE category_access SET access_control = {2} WHERE user_id = {accesscontrol.user_id} AND category_id = {accesscontrol.category_id}')
        return {"message": ['Access updated']}
    else:
        insert_query('INSERT INTO category_access(user_id, category_id, access_control) VALUES (%s, %s, %s)',
                     (accesscontrol.user_id, accesscontrol.category_id, 2))
        return {"message":
    [f'Access was set to WRITE to User with ID{accesscontrol.user_id} for Category with ID {accesscontrol.category_id}!']}


def read_access(accesscontrol: AccessControl):
    data = read_query('SELECT * FROM category_access WHERE user_id = %s AND category_id = %s',
                      (accesscontrol.user_id, accesscontrol.category_id))

    if any(data):
        update_query(
            f'UPDATE category_access SET access_control = {1} WHERE user_id = {accesscontrol.user_id} AND category_id = {accesscontrol.category_id}')
        return {"message": ['Access updated']}
    else:
        insert_query('INSERT INTO category_access(user_id, category_id, access_control) VALUES (%s, %s, %s)',
                     (accesscontrol.user_id, accesscontrol.category_id, 1))

        return f'Read access was given to User with ID{accesscontrol.user_id} for Category with ID {accesscontrol.category_id}!'


def revoke_access(accesscontrol: AccessControl):
    data = read_query('SELECT * FROM category_access WHERE user_id = %s AND category_id = %s',
                      (accesscontrol.user_id, accesscontrol.category_id))
    if any(data):
        update_query('DELETE FROM category_access WHERE user_id = %s', (accesscontrol.user_id,))

        return {"message":
    [f'Access to category with ID {accesscontrol.category_id} for user with ID {accesscontrol.user_id} was revoked!']}
    else:
        raise HTTPException(status_code=404,
                            detail=USER_NOT_FOUND)



def view_category_members(category_id):
    data = read_query('''
        SELECT ca.user_id, ca.category_id, ca.access_control, c.title AS category_title, u.username AS user_name
        FROM category_access AS ca
        JOIN category AS c ON ca.category_id = c.category_id
        JOIN users AS u ON ca.user_id = u.user_id
        WHERE ca.category_id = %s
    ''', (category_id,))
    return category_members_details(data)


def ban(user_id: int = Field(..., gt=0)):
    data = read_query('SELECT * FROM users WHERE user_id = %s AND is_banned = %s', (user_id, 0))
    if any(data):
        update_query(f'UPDATE users SET is_banned = {1} WHERE user_id = {user_id}')
        return {"message": f'User with ID {user_id} was successfully banned Forever!'}
    else:
        raise HTTPException(status_code=404, detail=f'No user with ID {user_id} was found among NON-Banned users!')


def format_user_details(user_details_list):
    return [{
        'User ID': user_detail[0],
        'Username': user_detail[1],
        'First name': user_detail[3],
        'Last name': user_detail[4],
        'role': user_detail[5],
        'E-mail:': user_detail[6],
        'Birth date:': user_detail[7]
    } for user_detail in user_details_list]


def category_members_details(data):
    return [
        {f'User ID': info[0],
         'Username': info[4],
         'Category ID': info[1],
         'Category Name': info[3],
         'Access level': 'Full access' if info[2] == 2 else 'Read Only'
         } for info in data
    ]
