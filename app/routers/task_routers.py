import os
import random
import string
from fastapi import HTTPException, APIRouter, status
from fastapi.responses import JSONResponse
from uuid import uuid4
from bson import ObjectId
from ..models.collections_model import Task, Tag, Log
from ..routers.tag_routers import create_tag
from ..utils.log_utils import create_log_entry
from db.settingsDB import settingsDB



router = APIRouter(prefix='/tasks', tags=['tasks'])



tasks_collection = settingsDB.COLLECTION_TASKS
tags_collection = settingsDB.COLLECTION_TAGS



@router.post("/")
async def create_task(tag: Tag):
    try:
        task_id = str(uuid4())  
        tag_id = str(uuid4()) 
        log_id = str(uuid4()) 

        task = Task(**{
            "task_id": task_id,
            "kwargs": tag.kwargs,
            "neuro_id": tag.neuro_id
        })

        created_task = await tasks_collection.insert_one(task.dict())

        tag = Tag(neuro_id=tag.neuro_id, kwargs=tag.kwargs, task_id=task_id, tag_id=tag_id)
        await tags_collection.insert_one(tag.dict())
        await create_tag(tag)
        log = await create_log_entry(task_id=task_id, tag_id=tag_id, log_id=log_id, rel_path_to_project=f"neuro/{tag.neuro_id}/{task_id}")

        return JSONResponse(content={"message": "Success!"}, status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {str(e)}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)



@router.get("/{task_id}")
async def get_task(task_id: str):
    try:
        # Проекция для исключения поля _id
        projection = {"_id": 0}
        task = await tasks_collection.find_one({"task_id": task_id}, projection=projection)

        if task:
            return JSONResponse(content=task, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"message": "Task not found"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {str(e)}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)



@router.delete("/{task_id}")
async def delete_task(task_id: str):
    try:
        result = await tasks_collection.delete_one({"task_id": task_id})
        if result.deleted_count == 1:
            return JSONResponse(content={"message": "Task deleted successfully"}, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"message": "Task not found"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {str(e)}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)



@router.put("/{task_id}")
async def update_task_args(task_id: str, new_kwargs: dict):
    try:
        result = await tasks_collection.update_one(
            {"task_id": task_id},
            {"$set": {"kwargs": new_kwargs}}
        )
        if result.modified_count == 1:
            return JSONResponse(content={"message": "Task args updated successfully"}, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"message": "Task not found"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {str(e)}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)