from fastapi import FastAPI
from app.routers import db_routers, tag_routers, task_routers, log_routers,  auth_routers
from db.settingsDB import SettingsDB


app = FastAPI()


app.include_router(tag_routers.router)
app.include_router(task_routers.router)
app.include_router(log_routers.router)
app.include_router(auth_routers.router)
