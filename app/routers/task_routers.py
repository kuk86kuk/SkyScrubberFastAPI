import os
import random
import string
import shutil

from fastapi import FastAPI, HTTPException, APIRouter, status, Depends
from fastapi.responses import JSONResponse
from typing import Optional
from pydantic import BaseModel
from uuid import uuid4
from bson import ObjectId
from ..models.collections_model import Task, Tag, Log
from ..routers.tag_routers import create_tag
from ..utils.log_utils import create_log_entry
from db.settingsDB import settingsDB
from ..utils.auth_utils import decode_jwt_token

#pip install fastapi uvicorn python-jose

router = APIRouter(prefix='/tasks', tags=['tasks'])


tasks_collection = settingsDB.COLLECTION_TASKS
tags_collection = settingsDB.COLLECTION_TAGS
logs_collection = settingsDB.COLLECTION_LOGS



@router.post("/")
async def create_task(tag: Tag, current_user: dict = Depends(decode_jwt_token)):
    '''
    POST функция: Создает задачу (task).

    Parameters:
    - tag: Объект типа Tag, содержащий информацию о задаче.
    
    Returns:
    JSONResponse с информацией о выполнении операции.
    - В случае успеха: "Success!" (статус 200 OK).
    - В случае ошибки: Сообщение об ошибке (статус 500 Internal Server Error).

    Описание:
       Эта функция обрабатывает POST-запросы для создания задачи. Она генерирует уникальные идентификаторы для задачи, тега и журнала. Затем создает объект задачи и тега, добавляет их в соответствующие коллекции, а также создает запись в журнале. Результат операции возвращается в виде JSONResponse.
    '''
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
        await create_tag(tag)

        log = await create_log_entry(task_id=task_id, tag_id=tag_id, log_id=log_id, rel_path_to_project=f"neuro/{tag.neuro_id}/{tag_id}", log_kwargs=tag.kwargs)

        return JSONResponse(content={"message": "Success!"}, status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {str(e)}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/{task_id}")
async def get_task(task_id: str, current_user: dict = Depends(decode_jwt_token)):
    '''
    GET функция: Получает информацию о задаче по её идентификатору.

    Parameters:
    - task_id: Идентификатор задачи, переданный в URL.

    Returns:
    JSONResponse с информацией о задаче или сообщением об отсутствии задачи.
    - В случае наличия задачи: Информация о задаче (статус 200 OK).
    - В случае отсутствия задачи: {"message": "Task not found"} (статус 404 Not Found).
    - В случае ошибки: Сообщение об ошибке (статус 500 Internal Server Error).

    Описание:
    Эта функция обрабатывает GET-запросы для получения информации о задаче по её идентификатору. Поиск осуществляется в базе данных по заданному идентификатору. Если задача найдена, её информация возвращается в виде JSONResponse. В противном случае возвращается сообщение о том, что задача не была найдена. В случае ошибки также возвращается соответствующее сообщение.
    '''
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
async def delete_task(task_id: str, current_user: dict = Depends(decode_jwt_token)):
    try:
        # Поиск логов связанных с задачей
        logs = await logs_collection.find({"task_id": task_id}).to_list(length=None)

        if not logs:
            raise HTTPException(status_code=404, detail="Logs for task not found")

        # Удаляем связанные данные
        for log in logs:
            # Удаление папки
            folder_path = log.get("path_to_project")
            shutil.rmtree(folder_path)  # Удаление папки

            # Удаление записи в MongoDB
            log_id = log.get("id")
            result = await logs_collection.delete_one({"id": log_id})

            if result.deleted_count != 1:
                raise HTTPException(status_code=500, detail="Error deleting log record")

            # Удаление записи в коллекции тегов по tag_id
            tag_id = log.get("tag_id")
            if tag_id:
                await tags_collection.delete_one({"tag_id": tag_id})

        # Затем удаляем саму задачу
        result = await tasks_collection.delete_one({"task_id": task_id})

        if result.deleted_count == 1:
            return JSONResponse(content={"message": "Task and related data deleted successfully"}, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"message": "Task not found"}, status_code=status.HTTP_404_NOT_FOUND)

    except HTTPException as he:
        raise he
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {str(e)}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/{task_id}")
async def update_task_args(task_id: str, new_kwargs: dict, current_user: dict = Depends(decode_jwt_token)):
    '''
    PUT функция: Обновляет аргументы задачи по её идентификатору.

    Parameters:
    - task_id: Идентификатор задачи, переданный в URL.
    - new_kwargs: Новые аргументы для обновления задачи.

    Returns:
    JSONResponse с информацией об успешном обновлении аргументов задачи или сообщением об отсутствии задачи.
    - В случае успешного обновления: {"message": "Task args updated successfully"} (статус 200 OK).
    - В случае отсутствия задачи: {"message": "Task not found"} (статус 404 Not Found).
    - В случае ошибки: Сообщение об ошибке (статус 500 Internal Server Error).

    Описание:
    Эта функция обрабатывает PUT-запросы для обновления аргументов задачи по её идентификатору. Поиск задачи в базе данных осуществляется по заданному идентификатору, и происходит обновление поля "kwargs" новыми аргументами. Если задача найдена и успешно обновлена, возвращается JSONResponse с сообщением об успешном обновлении. В случае, если задача не была найдена, возвращается сообщение о её отсутствии. В случае ошибки также возвращается соответствующее сообщение.
    '''
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