import logging

from fastapi import Depends, HTTPException, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from lib.database import fetch_routers, Session, get_db

router = APIRouter()


@router.get("/routers")
def get_routers(db: Session = Depends(get_db)):
    response = {"data": [], "err": None}

    try:
        response["data"] = [macs[0] for macs in fetch_routers(db).all()]
    except BaseException as e:
        logging.error(e)
        response["err"] = str(e)
        raise HTTPException(status_code=500, detail=response)

    return JSONResponse(content=jsonable_encoder(response))
