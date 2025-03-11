# Import the required services
from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from config.mongodb import init_db
from api.routes.box_router import router as box_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/", tags=["Health"])
async def root():
    return {"message": "Backend is up and running!"}


# Include the routers
app.include_router(router=box_router, prefix="/api", tags=["Boxes"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
