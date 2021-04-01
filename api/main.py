import logging
import uvicorn

from fastapi import FastAPI
from os import environ

from endpoints.all import router as all_router
from endpoints.routers import router as routers_router
from endpoints.lastseen import router as lastseen_router
from lib.ascii_banner import print_ascii_banner

app = FastAPI()
app.include_router(all_router)
app.include_router(routers_router)
app.include_router(lastseen_router)

if __name__ == "__main__":
    print_ascii_banner("MiniDetectorAPI")
    uvicorn.run(app, host="0.0.0.0", port=8000)
