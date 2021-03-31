import logging

from fastapi import Depends, HTTPException, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from lib.database import fetch_entities, Session, get_db

router = APIRouter()


@router.get("/all")
def get_entities(db: Session = Depends(get_db)):
    response = {"data": [], "err": None}

    try:
        response["data"] = [{"ip": ip, "mac": mac} for mac, ip in fetch_entities(db).all()]
    except BaseException as e:
        response["err"] = str(e)
        logging.error(e)
        raise HTTPException(status_code=500, detail=response)

    return JSONResponse(content=jsonable_encoder(response))
