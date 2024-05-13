from typing import Annotated
from services.categories_services import (check_category_by_name, check_all_existing_categories,
                                          create, delete_by_name, check_category_by_id)
from fastapi import APIRouter, Depends, HTTPException, Query
from models.models import Category
from services.login_services import get_current_user

categories_router = APIRouter(prefix='/categories')
user_dependency = Annotated[dict, Depends(get_current_user)]

NOT_AUTHORIZED = "Not authorized"
NOT_AUTHENTICATED = "Not authenticated"


@categories_router.get('', status_code=200)
async def check_all_categories(
    user: user_dependency,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    sort_by: str = Query(None, description="Column to sort by", alias="sort",
                         examples=["title", "category_id"]),
    search_query: str = Query(None, description="Search by name")
):
    """
    This method displays info about all existing categories with pagination, sorting, and search.
    """
    print(user)
    if user is None:
        raise HTTPException(status_code=401, detail=NOT_AUTHENTICATED)
    if user.get('role').lower() == 'user':
        raise HTTPException(status_code=403, detail=NOT_AUTHORIZED)

    result = await check_all_existing_categories(
        page=page, size=size, sort_by=sort_by, search_query=search_query
    )
    total_categories = result["Total Categories"]
    categories = result["Categories"]

    start = (page - 1) * size
    end = min(start + size, total_categories)
    paginated_categories = categories[start:end]

    return {
        "Categories": paginated_categories,
        "Total Categories": total_categories,
        "Page": page,
        "Size": size
    }


@categories_router.get('/{category_id:int}', status_code=200)
async def view_category(user: user_dependency, category_id: int):
    if user is None:
        raise HTTPException(status_code=401, detail=NOT_AUTHENTICATED)
    return await check_category_by_id(category_id)


@categories_router.get('/{category_name}', status_code=200)
async def get_by_name(user: user_dependency, category_name: str):
    """
    This method takes in the ID of the desired category and displays info about it.
    """
    if user is None:
        raise HTTPException(status_code=401, detail=NOT_AUTHENTICATED)
    if user.get('role').lower() == 'user':
        raise HTTPException(status_code=403, detail=NOT_AUTHORIZED)
    return await check_category_by_name(category_name)


@categories_router.post('/new', status_code=201)
async def new_category(user: user_dependency, category: Category):
    """
    This method takes the category name and creates a new category.
    """
    if user is None:
        raise HTTPException(status_code=401, detail=NOT_AUTHENTICATED)
    if user.get('role').lower() == 'user':
        raise HTTPException(status_code=403, detail=NOT_AUTHORIZED)
    return await create(category)


@categories_router.delete('', status_code=204)
async def delete_category(user: user_dependency, category_name: str):
    """
    This method takes the name of the category and deletes it.
    """
    if user is None:
        raise HTTPException(status_code=401, detail=NOT_AUTHENTICATED)
    if user.get('role').lower() == 'user':
        raise HTTPException(status_code=403, detail=NOT_AUTHORIZED)
    return await delete_by_name(category_name)
