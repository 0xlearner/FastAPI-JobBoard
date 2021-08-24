from fastapi import FastAPI
from core.config import settings
from db.session import engine
from db.base import Base
from routes import router_base
from web_apps.base import webapp_router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

origins = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router_base.api)
app.include_router(webapp_router)
app.mount("/static", StaticFiles(directory="static"), name="static")



@app.on_event("startup")
async def start_app():
    # create db tables on initializing
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)





