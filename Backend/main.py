from fastapi import FastAPI
from core.config import settings
from db.session import engine
from db.base_class import Base



app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

@app.on_event("startup")
async def start_app():
    # create db tables on initializing
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)




@app.get("/")
def hello_api():
    return {"message": "Welcome to Job Board"}



