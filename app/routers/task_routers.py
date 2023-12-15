import os
import random
import string

from fastapi import FastAPI, HTTPException, APIRouter, status, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import PyJWTError
from typing import Optional
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

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class TokenRequest(BaseModel):
    username: str
    password: str

@router.post("/token")
async def login_for_access_token(token_request: TokenRequest):
    # Пример простой логики аутентификации
    if token_request.username and token_request.password:
        user = token_request.username
        access_token = create_access_token(data={"sub": user})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        return {"error": "Invalid credentials"}

def create_access_token(data: dict):
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # здесь ты можешь валидировать и декодировать данные из токена
        # и использовать их для аутентификации пользователя
        # например, ты можешь получить идентификатор пользователя из payload и использовать его для аутентификации
    except PyJWTError:
        raise credentials_exception

@router.post("/create_task")
async def create_task(tag: Tag, current_user: dict = Depends(get_current_user)):
    try:
        task_id = str(uuid4())  # Генерируем уникальный task_id с помощью uuid4
        tag_id = str(uuid4()) # Генерируем уникальный tag_id с помощью uuid4
        log_id = str(uuid4()) # Генерируем уникальный tag_id с помощью uuid4

        task = Task(**{
            "task_id": task_id,
            "kwargs": tag.kwargs,
            "neuro_id": tag.neuro_id
        })

        created_task = await tasks_collection.insert_one(task.dict())

        tag = Tag(neuro_id=tag.neuro_id, kwargs=tag.kwargs, task_id=task_id, tag_id=tag_id)
        await tags_collection.insert_one(tag.dict())

        log = await create_log_entry(task_id=task_id, tag_id=tag_id, log_id=log_id, rel_path_to_project=f"neuro/{tag.neuro_id}/{task_id}")

        return JSONResponse(content={"message": "Success!"}, status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {str(e)}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get("/get_task/{task_id}")
async def get_task(task_id: str, current_user: dict = Depends(get_current_user)):
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
async def delete_task(task_id: str, current_user: dict = Depends(get_current_user)):
    try:
        result = await tasks_collection.delete_one({"task_id": task_id})
        if result.deleted_count == 1:
            return JSONResponse(content={"message": "Task deleted successfully"}, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"message": "Task not found"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {str(e)}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.put("/update_task_args/{task_id}")
async def update_task_args(task_id: str, new_kwargs: dict, current_user: dict = Depends(get_current_user)):
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