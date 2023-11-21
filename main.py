from fastapi import FastAPI
from app.routers import checks_directory_roytes, db_royters, processing_directory_royters



app = FastAPI()
app.include_router(checks_directory_roytes.router)
app.include_router(db_royters.router)
app.include_router(processing_directory_royters.router)