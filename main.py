from fastapi import FastAPI
from app.routers import db_routers, tag_routers, task_routers, progress_bar
from db.settingsDB import SettingsDB


app = FastAPI()



app.include_router(db_routers.router)
app.include_router(tag_routers.router)
app.include_router(task_routers.router)
app.include_router(progress_bar.router)