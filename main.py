from fastapi import FastAPI
from app.routers import db_routers, tag_routers, task_routers, progress_bar
from db.settingsDB import SettingsDB
from app.routers import db_routers, tag_routers, task_routers, log_routers, auth_routers


app = FastAPI()


app.include_router(db_routers.router)
app.include_router(tag_routers.router)
app.include_router(task_routers.router)
app.include_router(progress_bar.router)
app.include_router(log_routers.router)
app.include_router(auth_routers.router)