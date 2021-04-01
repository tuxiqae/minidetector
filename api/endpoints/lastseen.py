import logging

from fastapi import Depends, HTTPException, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from lib.database import fetch_lastseen, Session, get_db
from .statuses import statuses, status

router = APIRouter()


@router.get("/lastseen",
            description="Returns a JSON list of all mapped items by recency",
            responses=statuses)
def get_lastseen(db: Session = Depends(get_db)):
    """
    Fetches a list of (timestamp, MAC, IP) trios, ordered by recency

    :param db: Database session
    :return: JSONResponse
    """
    response = {"data": [], "err": None}

    try:
        response["data"] = [{"timestamp": ts, "ip": ip, "mac": mac} for ts, mac, ip in fetch_lastseen(db).all()]
    except BaseException as e:
        response["err"] = str(e)
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=response)

    return JSONResponse(content=jsonable_encoder(response))
