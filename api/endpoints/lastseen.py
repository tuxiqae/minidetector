import logging

from fastapi import Depends, HTTPException, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from lib.database import fetch_lastseen, Session, get_db

router = APIRouter()


@router.get("/lastseen")
def get_lastseen(db: Session = Depends(get_db)):
    response = {"data": [], "err": None}

    try:
        response["data"] = [{"timestamp": ts, "ip": ip, "mac": mac} for ts, mac, ip in fetch_lastseen(db).all()]
    except BaseException as e:
        response["err"] = str(e)
        logging.error(e)
        raise HTTPException(status_code=500, detail=response)

    return JSONResponse(content=jsonable_encoder(response))
