import os

from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson import ObjectId
from db.settingsDB import SettingsDB
from ..models.collections_model import Task, Tag, Log

router = APIRouter(prefix='/tags', tags=['tags'])

settingsDB = SettingsDB()

tags_collection = settingsDB.COLLECTION_TAGS
logs_collection = settingsDB.COLLECTION_LOGS

@router.post("/create_tag")
async def create_tag(tag: Tag):
    try:
        created_tag = await tags_collection.insert_one(tag.dict())

        tag_folder_path = f"neuro/{tag.neuro_id}/{str(created_tag.inserted_id)}"
        os.makedirs(tag_folder_path, exist_ok=True)

        return JSONResponse(content={}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# async def get_task(task_id: str):
#     task = await collection.find_one({"_id": ObjectId(task_id)})
#     return task

# @router.get("/get_task/{task_id}", response_model=Task)
# async def read_task(task_id: str):
#     task = await get_task(task_id)
#     if task:
#         return task
#     else:
#         raise HTTPException(status_code=404, detail="Task not found")
    
# @router.delete("/delete_task/{task_id}", response_model=Task)
# async def delete_task(task_id: str):
#     task = await get_task(task_id)
#     if task:
#         # Удаляем задачу
#         await collection.delete_one({"_id": ObjectId(task_id)})
#         return task
#     else:
#         raise HTTPException(status_code=404, detail="Task not found")
    
# @router.put("/update_task/{task_id}", response_model=Task)
# async def update_task(task_id: str, updated_task: dict):
#     existing_task = await get_task(task_id)
#     if existing_task:
#         # Обновляем поле только поле description!!!
#         await collection.update_one(
#             {"_id": ObjectId(task_id)},
#             {"$set": {"description": updated_task["description"]}}
#         )
#         # Получаем обновленную задачу
#         updated_task = await get_task(task_id)
#         return updated_task
#     else:
#         raise HTTPException(status_code=404, detail="Task not found")