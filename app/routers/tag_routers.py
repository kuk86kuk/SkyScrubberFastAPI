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

@router.get("/get_tag/{tag_id}")
async def get_tag(tag_id: str):
    try:
        tag = await tags_collection.find_one({"_id": ObjectId(tag_id)})
        if tag:
            # Преобразование ObjectId в строку
            tag["_id"] = str(tag["_id"])
            return JSONResponse(content=tag, status_code=200)
        else:
            raise HTTPException(status_code=404, detail=f"Tag not found for id: {tag_id}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete_tag/{tag_id}")
async def delete_tag(tag_id: str):
    try:
        result = await tags_collection.delete_one({"_id": ObjectId(tag_id)})
        if result.deleted_count == 1:
            return JSONResponse(content={"message": "Tag deleted successfully"}, status_code=200)
        else:
            raise HTTPException(status_code=404, detail="Tag not found")
    except Exception as e:
        error_message = f"Error in delete_tag: {e}"
        print(error_message)
        raise HTTPException(status_code=500, detail=error_message)

@router.put("/update_tag_args/{tag_id}")
async def update_tag_args(tag_id: str, new_args: dict):
    try:
        result = await tags_collection.update_one(
            {"_id": ObjectId(tag_id)},
            {"$set": {"args": new_args}}
        )
        if result.modified_count == 1:
            return JSONResponse(content={"message": "Tag args updated successfully"}, status_code=200)
        else:
            raise HTTPException(status_code=404, detail="Tag not found")
    except Exception as e:
        error_message = f"Error in update_tag_args: {e}"
        print(error_message)
        raise HTTPException(status_code=500, detail=error_message)

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