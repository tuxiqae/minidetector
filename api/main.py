import logging
import uvicorn
from fastapi import FastAPI
from os import environ

from endpoints.all import router as all_router
from endpoints.routers import router as routers_router
from endpoints.lastseen import router as lastseen_router
from lib.ascii_banner import print_ascii_banner

app = FastAPI(docs_url="/",
              redoc_url="/redoc",
              openapi_tags=[{"name": "Entities", "description": "Fetch entities from the DB"}])

app.include_router(all_router)
app.include_router(routers_router)
app.include_router(lastseen_router)

if __name__ == "__main__":
    print_ascii_banner("MiniDetectorAPI")
    try:
        port = environ["API_PORT"]
        uvicorn.run(app, host="0.0.0.0", port=int(port))
    except KeyError:
        raise KeyError("Could not fetch the environment variable `API_PORT`")
    except Exception as e:
        logging.exception(e)
        exit(1)
