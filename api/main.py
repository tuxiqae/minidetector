import uvicorn
import logging

from fastapi import Depends, FastAPI, HTTPException
from lib.database import fetch_entities, create_session, Session, fetch_routers, fetch_lastseen
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

app = FastAPI()


# Dependency
def get_db():
    db = create_session()
    try:
        yield db
    finally:
        db.close()


@app.get("/all")
def get_entities(db: Session = Depends(get_db)):
    response = {"data": [], "err": None}

    try:
        response["data"] = [{"ip": ip, "mac": mac} for mac, ip in fetch_entities(db).all()]
    except BaseException as e:
        response["err"] = str(e)
        logging.error(e)
        raise HTTPException(status_code=500, detail=response)

    return JSONResponse(content=jsonable_encoder(response))


@app.get("/routers")
def get_routers(db: Session = Depends(get_db)):
    response = {"data": [], "err": None}

    try:
        response["data"] = [macs[0] for macs in fetch_routers(db).all()]
    except BaseException as e:
        logging.error(e)
        response["err"] = str(e)
        raise HTTPException(status_code=500, detail=response)

    return JSONResponse(content=jsonable_encoder(response))


@app.get("/lastseen")
def get_lastseen(db: Session = Depends(get_db)):
    response = {"data": [], "err": None}

    try:
        response["data"] = [{"timestamp": ts, "ip": ip, "mac": mac} for ts, mac, ip in fetch_lastseen(db).all()]
    except BaseException as e:
        response["err"] = str(e)
        logging.error(e)
        raise HTTPException(status_code=500, detail=response)

    return JSONResponse(content=jsonable_encoder(response))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
