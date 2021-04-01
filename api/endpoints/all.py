import logging

from fastapi import Depends, HTTPException, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from lib.database import fetch_entities, Session, get_db
from .statuses import statuses, status

router = APIRouter()


@router.get("/all",
            description="Returns a JSON list of all mapped entities",
            responses=statuses)
def get_entities(db: Session = Depends(get_db)) -> JSONResponse:
    """
    Fetches all entities from the DB and returns them as a list (MAC, IP) tuples

    :param db: Database session
    :return: JSONResponse
    """
    response = {"data": [], "err": None}

    try:
        response["data"] = [{"ip": ip, "mac": mac} for mac, ip in fetch_entities(db).all()]
    except Exception as e:
        response["err"] = str(e)
        logging.exception(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=response)

    return JSONResponse(content=jsonable_encoder(response))
