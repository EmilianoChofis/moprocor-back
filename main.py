from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Boxes API", description="Backend with MongoDB and AWS services")


@app.get("/", tags=["Health"])
async def root():
    return {"message": "Backend is up and running!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
