from fastapi import FastAPI
from app.routers import check_directory_routers, db_routers, processing_directory_routers, tag_routers,task_routers,log_routers



app = FastAPI()
app.include_router(check_directory_routers.router)
app.include_router(db_routers.router)
app.include_router(processing_directory_routers.router)
app.include_router(tag_routers.router)
app.include_router(task_routers.router)
app.include_router(log_routers.router)