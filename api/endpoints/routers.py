import logging

from fastapi import Depends, HTTPException, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from lib.database import fetch_routers, Session, get_db
from .statuses import statuses, status

router = APIRouter()


@router.get("/routers",
            description="Returns the MAC addresses of all mapped routers",
            responses=statuses)
def get_routers(db: Session = Depends(get_db)) -> JSONResponse:
    """
    Fetches a list of MAC addresses for all MAC addresses which appears in more than 3 entities

    :param db: Database session
    :return: JSONResponse
    """
    response = {"data": [], "err": None}

    try:
        response["data"] = [macs[0] for macs in fetch_routers(db).all()]
    except Exception as e:
        logging.exception(e)
        response["err"] = str(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=response)

    return JSONResponse(content=jsonable_encoder(response))
