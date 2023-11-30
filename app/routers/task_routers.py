import os

from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson import ObjectId
from db.settingsDB import SettingsDB
from ..models.collections_model import Task, Tag, Log
from ..routers.tag_routers import create_tag
 

router = APIRouter(prefix='/tasks', tags=['tasks'])

settingsDB = SettingsDB()

tasks_collection = settingsDB.COLLECTION_TASKS

# Эндпоинт для тестов, чтобы имитировать работу Task Manager'а
@router.post("/create_task")
async def create_task(tag: Tag):
    try:
        task = Task(**{
            "args": tag.args,
            "neuro_id": tag.neuro_id
        })

        created_task = await tasks_collection.insert_one(task.dict())
        # Получаем автоматически сгенерированный _id
        task_id = str(created_task.inserted_id)

        # Создаем объект Tag внутри эндпоинта, используя тот же _id
        tag = Tag(neuro_id=tag.neuro_id, args=tag.args)

        # Подставляем _id
        tag.id = task_id
        await create_tag(tag)

        return JSONResponse(content={}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))