from fastapi import Depends, Query


def get_pagination(skip: int = 0, limit: int = Query(default=10, le=100)):
    return {"skip": skip, "limit": limit}


def get_current_page(
    pagination: dict = Depends(get_pagination),
):
    return pagination["skip"] // pagination["limit"] + 1