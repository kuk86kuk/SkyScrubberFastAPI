import os
import random
import string

from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson import ObjectId
from db.settingsDB import SettingsDB
from ..models.collections_model import Task, Tag, Log
from ..routers.tag_routers import create_tag
from ..utils.log_utils import create_log_entry

router = APIRouter(prefix='/tasks', tags=['tasks'])

settingsDB = SettingsDB()

tasks_collection = settingsDB.COLLECTION_TASKS
tags_collection = settingsDB.COLLECTION_TAGS

@router.post("/create_task")
async def create_task(tag: Tag):
    try:
        task = Task(**{
            "args": tag.args,
            "neuro_id": tag.neuro_id
        })

        created_task = await tasks_collection.insert_one(task.dict())
        task_id = str(created_task.inserted_id)

        tag = Tag(neuro_id=tag.neuro_id, args=tag.args, task_id=task_id)
        await tags_collection.insert_one(tag.dict())

        log = await create_log_entry(tag_id=task_id, rel_path_to_project=f"neuro/{tag.neuro_id}/{task_id}")

        return JSONResponse(content={}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_task/{task_id}")
async def get_task(task_id: str):
    try:
        task = await tasks_collection.find_one({"_id": ObjectId(task_id)})
        if task:
            # Преобразование ObjectId в строку
            task["_id"] = str(task["_id"])
            return JSONResponse(content=task, status_code=200)
        else:
            raise HTTPException(status_code=404, detail="Task not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete_task/{task_id}")
async def delete_task(task_id: str):
    try:
        result = await tasks_collection.delete_one({"_id": ObjectId(task_id)})
        if result.deleted_count == 1:
            return JSONResponse(content={"message": "Task deleted successfully"}, status_code=200)
        else:
            raise HTTPException(status_code=404, detail="Task not found")
    except Exception as e:
        error_message = f"Error in delete_task: {e}"
        print(error_message)
        raise HTTPException(status_code=500, detail=error_message)

@router.put("/update_task_args/{task_id}")
async def update_task_args(task_id: str, new_args: dict):
    try:
        result = await tasks_collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": {"args": new_args}}
        )
        if result.modified_count == 1:
            return JSONResponse(content={"message": "Task args updated successfully"}, status_code=200)
        else:
            raise HTTPException(status_code=404, detail="Task not found")
    except Exception as e:
        error_message = f"Error in update_task_args: {e}"
        print(error_message)
        raise HTTPException(status_code=500, detail=error_message)