import logging
from fastapi import APIRouter, HTTPException

from PROJECT_NAME.log import Logger
from PROJECT_NAME.models.response import ErrorResponse


router = APIRouter()


@router.post("/")
async def create_card(payload: Payload, debug: bool = False):
    """
        A route to ...
    """
    try:
        log = Logger()

    except Exception as err:

        log.create_log(payload=payload,
                       details=str(err))

        error_response = ErrorResponse(
            status="error",
            details=str(err)
        )
        raise HTTPException(status_code=400,
                            detail=error_response.model_dump())
