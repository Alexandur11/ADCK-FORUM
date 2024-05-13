from data.database import read_query, update_query
from fastapi import HTTPException
from pydantic import Field


def promote(user_id: int = Field(..., gt=0)):
    data = read_query('SELECT * FROM users '
                      'WHERE user_id = %s AND role = %s', (user_id, 'user'))
    if any(data):
        update_query('UPDATE users SET role = %s WHERE user_id = %s', ('admin', user_id))
        return {"message": ['User Promoted']}
    else:
        raise HTTPException(status_code=404,
                            detail=f'This Account is already an Admin or Account with ID {user_id} does not exist')


def demote(user_id: int = Field(..., gt=0)):
    data = read_query('SELECT * FROM users '
                      'WHERE user_id = %s AND role = %s', (user_id, 'admin'))
    if any(data):
        update_query('UPDATE users SET role = %s WHERE user_id = %s', ('user', user_id))
        return {"message": ['User Demoted']}
    else:
        raise HTTPException(status_code=404,
                            detail=f'This Account is not an Admin or Account with ID {user_id} does not exist')


def delete_admin_account(admin_id: int = Field(..., gt=0)):
    data = read_query('SELECT * FROM users '
                      'WHERE user_id = %s AND role = %s', (admin_id, 'admin'))
    if any(data):
        update_query((
            f"UPDATE users "
            f"SET username = 'Default{admin_id}', "
            f"password = 'MasterPancakes1', "
            f"firstname = NULL, "
            f"lastname = NULL, "
            f"email = NULL, "
            f"birth_date = NULL "
            f"WHERE user_id = %s"), (admin_id,))
        return {'message': ['User deleted successfully!']}
    else:
        raise HTTPException(status_code=404,
                            detail=f'This Account is not an Admin or does not exist!')

# def check_admin_status(user_id: int):
#     user_list = get_user_by_id(user_id)
#     if user_list:
#         for user in user_list:
#             if user.get(IS_ADMIN) == 'No':
#                 return {'message': 'This user is not an admin.'}
#             else:
#                 return {'message': 'This user is an admin.'}
#     else:
#         raise HTTPException(status_code=404, detail=USER_NOT_FOUND)
