from typing import Annotated
from starlette import status
from fastapi import APIRouter, Depends, HTTPException
from models.models import AccessControl
from services.admin_services import (get_all_users, get_user_by_id,
                                     get_user_by_username, delete_user_by_id,
                                     check_if_user_is_logged, check_all_logged,
                                     lock_topic, unlock_topic,
                                     lock_category, unlock_category, ban, write_access, read_access, revoke_access,
                                     view_category_members)
from services.login_services import get_current_user

admin_router = APIRouter(prefix='/admin_panel')
user_dependency = Annotated[dict, Depends(get_current_user)]

NOT_AUTHORIZED = "Not authorized"
NOT_AUTHENTICATED = "Not authenticated"


@admin_router.get(path='/users/all', status_code=200)
async def get_all(user: user_dependency):
    """
    This method shows all currently registered users
    """
    if user is None:
        raise HTTPException(status_code=401, detail=NOT_AUTHENTICATED)
    if user.get('role').lower() == 'user':
        raise HTTPException(status_code=403, detail=NOT_AUTHORIZED)
    return get_all_users()


@admin_router.get(path='/users/idsearch/{user_id}', status_code=200)
async def search_user_by_id(user: user_dependency, user_id: int):
    """
    This method takes in an ID and shows info about the user it belongs to
    """
    if user is None:
        raise HTTPException(status_code=401, detail=NOT_AUTHENTICATED)
    if user.get('role').lower() == 'user':
        raise HTTPException(status_code=403, detail=NOT_AUTHORIZED)
    return get_user_by_id(user_id)


@admin_router.get(path='/users/search/{username}', status_code=200)
async def search_user_by_username(user: user_dependency, username: str):
    """
    This method takes in a username and shows info about the user it belongs to
    """
    if user is None:
        raise HTTPException(status_code=401, detail=NOT_AUTHENTICATED)
    if user.get('role').lower() == 'user':
        raise HTTPException(status_code=403, detail=NOT_AUTHORIZED)
    return get_user_by_username(username)


@admin_router.get(path='/users/logged/{user_id}', status_code=200)
async def is_logged(user: user_dependency, user_id: int):
    """
    This method takes in an ID and tells you whether the user it belongs to is currently logged in
    """
    if user is None:
        raise HTTPException(status_code=401, detail=NOT_AUTHENTICATED)
    if user.get('role').lower() == 'user':
        raise HTTPException(status_code=403, detail=NOT_AUTHORIZED)
    return check_if_user_is_logged(user_id)


@admin_router.get(path='/users/all/logged_now', status_code=200)
async def all_logged(user: user_dependency):
    """
    This method shows you of the currently logged-in users
    """
    if user is None:
        raise HTTPException(status_code=401, detail=NOT_AUTHENTICATED)
    if user.get('role').lower() == 'user':
        raise HTTPException(status_code=403, detail=NOT_AUTHORIZED)
    return check_all_logged()


@admin_router.delete(path='/user{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user: user_dependency, user_id: int):
    """
    This method takes in an ID and deletes the user it belongs to
    """
    if user is None:
        raise HTTPException(status_code=401, detail=NOT_AUTHENTICATED)
    if user.get('role').lower() == 'user':
        raise HTTPException(status_code=403, detail=NOT_AUTHORIZED)
    return delete_user_by_id(user_id)


@admin_router.put(path='/actions/topics/lock/{topic_id}', status_code=200)
async def lock_topic_by_id(user: user_dependency, topic_id: int):
    """
    This method locks the desired Topic by its ID.
    """
    if user is None:
        raise HTTPException(status_code=401, detail=NOT_AUTHENTICATED)
    if user.get('role').lower() == 'user':
        raise HTTPException(status_code=403, detail=NOT_AUTHORIZED)
    return lock_topic(topic_id)


@admin_router.put(path='/actions/topics/unlock/{topic_id}', status_code=200)
async def unlock_topic_by_id(user: user_dependency, topic_id: int):
    """
    This method unlocks the desired Topic by its ID.
    """
    if user is None:
        raise HTTPException(status_code=401, detail=NOT_AUTHENTICATED)
    if user.get('role').lower() == 'user':
        raise HTTPException(status_code=403, detail=NOT_AUTHORIZED)
    return unlock_topic(topic_id)


@admin_router.put(path='/actions/categories/lock/{category_id}', status_code=200)
async def lock_category_by_id(user: user_dependency, category_id: int):
    """
    This method locks the desired Category by its ID.
    """
    if user is None:
        raise HTTPException(status_code=401, detail=NOT_AUTHENTICATED)
    if user.get('role').lower() == 'user':
        raise HTTPException(status_code=403, detail=NOT_AUTHORIZED)
    return lock_category(category_id)


@admin_router.put(path='/actions/categories/unlock/{category_id}', status_code=200)
async def unlock_category_by_id(user: user_dependency, category_id: int):
    """
    This method unlocks the desired Category by its ID.
    """
    if user is None:
        raise HTTPException(status_code=401, detail=NOT_AUTHENTICATED)
    if user.get('role').lower() == 'user':
        raise HTTPException(status_code=403, detail=NOT_AUTHORIZED)
    return unlock_category(category_id)


@admin_router.put(path='/actions/users/ban/{user_id}', status_code=200)
async def ban_user_by_id(user: user_dependency, user_id: int):
    """
    This method bans the desired user by its ID.
    """
    if user is None:
        raise HTTPException(status_code=401, detail=NOT_AUTHENTICATED)
    if user.get('role').lower() == 'user':
        raise HTTPException(status_code=403, detail=NOT_AUTHORIZED)
    return ban(user_id)


@admin_router.put(path='/actions/users/write_access', status_code=200)
async def give_write(user: user_dependency, accesscontrol: AccessControl):
    """
    This method gives write permissions to a desired user.
    """
    if user is None:
        raise HTTPException(status_code=401, detail=NOT_AUTHENTICATED)
    if user.get('role').lower() == 'user':
        raise HTTPException(status_code=403, detail=NOT_AUTHORIZED)
    return write_access(accesscontrol)


@admin_router.put(path="/actions/users/read_access", status_code=200)
async def give_read(user: user_dependency, accesscontrol: AccessControl):
    """
    This method gives read-only permission to the desired user.
    """
    if user is None:
        raise HTTPException(status_code=401, detail=NOT_AUTHENTICATED)
    if user.get('role').lower() == 'user':
        raise HTTPException(status_code=403, detail=NOT_AUTHORIZED)
    return read_access(accesscontrol)


@admin_router.put(path="/actions/users/no_access", status_code=200)
async def revoke(user: user_dependency, accesscontrol: AccessControl):
    """
    This method revokes the access of the desired user from the desired category.
    """
    if user is None:
        raise HTTPException(status_code=401, detail=NOT_AUTHENTICATED)
    if user.get('role').lower() == 'user':
        raise HTTPException(status_code=403, detail=NOT_AUTHORIZED)
    return revoke_access(accesscontrol)


@admin_router.get('/actions/categories/members/{category_id}', status_code=200)
async def category_members(user: user_dependency, category_id):
    if user is None:
        raise HTTPException(status_code=401, detail=NOT_AUTHENTICATED)
    if user.get('role').lower() == 'user':
        raise HTTPException(status_code=403, detail=NOT_AUTHORIZED)
    return view_category_members(category_id)
