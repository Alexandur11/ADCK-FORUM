from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from services.forum_owner_services import promote, demote, delete_admin_account
from services.login_services import get_current_user

owner_router = APIRouter(prefix='/owner_panel')
user_dependency = Annotated[dict, Depends(get_current_user)]

NOT_AUTHORIZED = "Not authorized"
NOT_AUTHENTICATED = "Not authenticated"


# @owner_router.get('/{user_id}/status', status_code=200)
# async def check_user_admin_status(user_id: int):
#     return check_admin_status(user_id)


@owner_router.put('/promote/{user_id}', status_code=201)
async def create_admin(user: user_dependency, user_id: int):
    """
    This method takes the desired ID and turns the corresponding user into an ADMIN.
    """
    if user is None:
        raise HTTPException(status_code=401, detail=NOT_AUTHENTICATED)
    if user.get('role').lower() != 'owner':
        raise HTTPException(status_code=403, detail=NOT_AUTHORIZED)
    return promote(user_id)



@owner_router.put('/demote/{user_id}', status_code=201)
async def demote_admin(user: user_dependency, user_id: int):
    """
    This method takes the desired ID and strips the corresponding user from his ADMIN rights.
    """
    if user is None:
        raise HTTPException(status_code=401, detail=NOT_AUTHENTICATED)
    if user.get('role').lower() != 'owner':
        raise HTTPException(status_code=403, detail=NOT_AUTHORIZED)
    return demote(user_id)



@owner_router.delete(path='/{admin_id}', status_code=204)
async def delete_admin(user: user_dependency, admin_id: int):
    """
    This method takes the desired ID, checks for any matches,
    and if found it entirely removed the user.
    """
    if user is None:
        raise HTTPException(status_code=401, detail=NOT_AUTHENTICATED)
    if user.get('role').lower() != 'owner':
        raise HTTPException(status_code=403, detail=NOT_AUTHORIZED)
    delete_admin_account(admin_id)
    return f'Admin account with ID {admin_id} successfully deleted'
