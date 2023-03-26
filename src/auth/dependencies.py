from typing import Optional
from typing_extensions import Annotated
from fastapi import Depends, Query


def pagination(skip: int = 0, limit: int = 10) -> dict:
    return {
        'skip': skip,
        'limit': limit,
    }


PaginationDep = Annotated[dict, Depends(pagination)]
