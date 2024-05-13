from services.login_services import generate_token
import os

NOT_AUTHORIZED = "Not authorized"
NOT_AUTHENTICATED = "Not authenticated"
USER_NOT_FOUND = 'User not found!'
IS_ADMIN = 'Is admin'
secret_key = os.getenv("SECRET_KEY")


def user_mock():
    data = {"sub": 'Hristo', "user_id": 1, "role": 'user'}
    user_token = generate_token(data)
    info = {"access_token": user_token, "token_type": "bearer"}
    return info.get('access_token')


def admin_mock():
    data = {"sub": 'Hristo', "user_id": 1, "role": 'admin'}
    user_token = generate_token(data)
    info = {"access_token": user_token, "token_type": "bearer"}
    return info.get('access_token')

def owner_mock():
    data = {"sub": 'Hristo', "user_id": 1, "role": 'owner'}
    user_token = generate_token(data)
    info ={"access_token": user_token, "token_type": "bearer"}
    return info.get('access_token')
