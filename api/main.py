import uvicorn

from fastapi import FastAPI
from endpoints.all import router as all_router
from endpoints.routers import router as routers_router
from endpoints.lastseen import router as lastseen_router

app = FastAPI()
app.include_router(all_router)
app.include_router(routers_router)
app.include_router(lastseen_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
