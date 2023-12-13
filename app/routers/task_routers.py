import os
import random
import string

from fastapi import FastAPI, HTTPException, APIRouter, status
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from uuid import uuid4
from bson import ObjectId
from db.settingsDB import SettingsDB
from ..models.collections_model import Task, Tag, Log
from ..routers.tag_routers import create_tag
from ..utils.log_utils import create_log_entry

router = APIRouter(prefix='/tasks', tags=['tasks'])

settingsDB = SettingsDB()

tasks_collection = settingsDB.COLLECTION_TASKS
tags_collection = settingsDB.COLLECTION_TAGS

@router.post("/create_task", status_code=status.HTTP_200_OK)
async def create_task(tag: Tag):
    try:
        task_id = str(uuid4())  # Генерируем уникальный task_id с помощью uuid4
        tag_id = str(uuid4()) # Генерируем уникальный tag_id с помощью uuid4

        task = Task(**{
            "task_id": task_id,
            "args": tag.args,
            "neuro_id": tag.neuro_id
        })

        created_task = await tasks_collection.insert_one(task.dict())

        tag = Tag(neuro_id=tag.neuro_id, args=tag.args, task_id=task_id, tag_id=tag_id)
        await tags_collection.insert_one(tag.dict())

        log = await create_log_entry(task_id=task_id, tag_id=tag_id, rel_path_to_project=f"neuro/{tag.neuro_id}/{task_id}")

        return JSONResponse(content={"message": "Success!"}, status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {str(e)}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get("/get_task/{task_id}")
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

@router.delete("/delete_task/{task_id}")
async def delete_task(task_id: str):
    try:
        result = await tasks_collection.delete_one({"task_id": task_id})
        if result.deleted_count == 1:
            return JSONResponse(content={"message": "Task deleted successfully"}, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"message": "Task not found"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {str(e)}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.put("/update_task_args/{task_id}")
async def update_task_args(task_id: str, new_args: dict):
    try:
        result = await tasks_collection.update_one(
            {"task_id": task_id},
            {"$set": {"args": new_args}}
        )
        if result.modified_count == 1:
            return JSONResponse(content={"message": "Task args updated successfully"}, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"message": "Task not found"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {str(e)}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)