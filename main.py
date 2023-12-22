from fastapi import FastAPI
from app.routers import db_routers, tag_routers, task_routers, log_routers, progress_bar, auth_routers
from db.settingsDB import SettingsDB


app = FastAPI()


app.include_router(db_routers.router)
app.include_router(tag_routers.router)
app.include_router(task_routers.router)
app.include_router(progress_bar.router)
app.include_router(log_routers.router)
app.include_router(auth_routers.router)
