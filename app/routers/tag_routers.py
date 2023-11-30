from fastapi import APIRouter
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson import ObjectId
from db.settingsDB import SettingsDB

import os

router = APIRouter(prefix='/tags', tags=['tags'])
settingsDB = SettingsDB()

tasks_collection = settingsDB.COLLECTION_TASKS

# Подключение к MongoDB
# client = AsyncIOMotorClient("mongodb://localhost:27017")
# db = client["tasks"]
# collection = db["tasks"]

# Обновленная модель данных для задачи без поля id
class Task(BaseModel):
    description: str
    neuro_id: str

# Роут для создания задачи
@router.post("/create_task")
async def create_task(task: Task):
    try:
        # Добавляем задачу в MongoDB
        created_task = await tasks_collection.insert_one(task.dict())

        # Создаем папку для задачи внутри папки neuro
        task_folder_path = f"neuro/{task.neuro_id}/{str(created_task.inserted_id)}"
        os.makedirs(task_folder_path, exist_ok=True)

        # Возвращаем успешный ответ
        return {"message": "Task created successfully"}
    except Exception as e:
        # Если произошла ошибка, возвращаем ошибку сервера
        raise HTTPException(status_code=500, detail=str(e))

async def get_task(task_id: str):
    task = await collection.find_one({"_id": ObjectId(task_id)})
    return task

@router.get("/get_task/{task_id}", response_model=Task)
async def read_task(task_id: str):
    task = await get_task(task_id)
    if task:
        return task
    else:
        raise HTTPException(status_code=404, detail="Task not found")
    
@router.delete("/delete_task/{task_id}", response_model=Task)
async def delete_task(task_id: str):
    task = await get_task(task_id)
    if task:
        # Удаляем задачу
        await collection.delete_one({"_id": ObjectId(task_id)})
        return task
    else:
        raise HTTPException(status_code=404, detail="Task not found")
    
@router.put("/update_task/{task_id}", response_model=Task)
async def update_task(task_id: str, updated_task: dict):
    existing_task = await get_task(task_id)
    if existing_task:
        # Обновляем поле только поле description!!!
        await collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": {"description": updated_task["description"]}}
        )
        # Получаем обновленную задачу
        updated_task = await get_task(task_id)
        return updated_task
    else:
        raise HTTPException(status_code=404, detail="Task not found")