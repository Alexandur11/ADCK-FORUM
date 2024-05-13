from fastapi import APIRouter


users_router = APIRouter(prefix='/user_panel')

@users_router.get('', status_code=200)
def user_home():
    return "Welcome to your user page"


