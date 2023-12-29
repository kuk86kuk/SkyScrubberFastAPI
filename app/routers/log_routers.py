import os
import random
import string

from fastapi import FastAPI, HTTPException, APIRouter, status, Depends, Body
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from uuid import uuid4
from bson import ObjectId
from db.settingsDB import SettingsDB
from ..models.collections_model import Task, Tag, Log
from ..routers.tag_routers import create_tag
from ..utils.log_utils import create_log_entry
from ..utils.auth_utils import decode_jwt_token
from typing import List
import logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix='/logs', tags=['logs'])

settingsDB = SettingsDB()

logs_collection = settingsDB.COLLECTION_LOGS

from fastapi import HTTPException, Query

@router.get("/")
async def get_logs(task_id: str = Query(None), tag_id: str = Query(None), current_user: dict = Depends(decode_jwt_token)):
    '''
    GET функция: Получает логи по заданным параметрам.

    Parameters:
    - task_id: Идентификатор задачи (необязательный параметр).
    - tag_id: Идентификатор тега (необязательный параметр).

    Returns:
    JSONResponse с информацией о логе или сообщением об отсутствии лога.
    - В случае наличия лога: Информация о логе (статус 200 OK).
    - В случае отсутствия лога: {"message": "Log not found"} (статус 404 Not Found).
    - В случае ошибки: Сообщение об ошибке (статус 500 Internal Server Error).

    Описание:
    Эта функция обрабатывает GET-запросы для получения логов по заданным параметрам (task_id, tag_id). Если хотя бы один из параметров предоставлен, производится поиск логов в базе данных. Результат запроса преобразуется в объект Log и возвращается в виде JSONResponse. В случае, если лог не был найден, возвращается сообщение об отсутствии лога с соответствующим статусом. В случае ошибки также возвращается соответствующее сообщение.
    '''
    try:
        # Проверка, что хотя бы один из параметров задан
        if not task_id and not tag_id:
            raise HTTPException(status_code=400, detail="Either task_id or tag_id must be provided")

        # Поиск логов по заданным task_id и/или tag_id
        query_params = {}
        if task_id:
            query_params["task_id"] = task_id
        if tag_id:
            query_params["tag_id"] = tag_id

        log = await logs_collection.find_one(query_params)

        if log:
            # Преобразование результатов запроса в объект Log
            log_obj = Log(**log)
            log_obj.register_date = log_obj.register_date.isoformat()

            return JSONResponse(content={"log": log_obj.dict()}, status_code=status.HTTP_200_OK) 
        else:
            # Если лог не найден, возвращаем ошибку 404
            raise HTTPException(status_code=404, detail="Log not found")
    except Exception as e:
     logger.error(f"Error: {str(e)}", exc_info=True)
    return JSONResponse(content={"message": "Internal Server Error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.delete("/")
async def delete_log(task_id: str = Query(None), tag_id: str = Query(None), current_user: dict = Depends(decode_jwt_token)):
    try:
        # Проверка, что хотя бы один из параметров задан
        if not task_id and not tag_id:
            raise HTTPException(status_code=400, detail="Either task_id or tag_id must be provided")

        # Удаляем записи в логах в зависимости от параметра
        if task_id:
            # Удаляем все записи в логах по task_id
            result = await logs_collection.delete_many({"task_id": task_id})
        elif tag_id:
            # Удаляем все записи в логах по tag_id
            result = await logs_collection.delete_many({"tag_id": tag_id})

        if result.deleted_count >= 1:
            return JSONResponse(content={"message": "Log(s) deleted successfully"}, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"message": "Log(s) not found"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {str(e)}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/")
async def update_log(task_id: str = Query(None), tag_id: str = Query(None), updated_log: Log = Body(...), current_user: dict = Depends(decode_jwt_token)):
    try:
        # Проверка, что хотя бы один из параметров задан
        if not task_id and not tag_id:
            raise HTTPException(status_code=400, detail="Either task_id or tag_id must be provided")

        # Выполняем обновление записи в логах в зависимости от параметра
        if task_id:
            # Обновляем записи в логах по task_id
              print(f"Updating logs with task_id: {task_id}")
              result = await logs_collection.update_many({"task_id": task_id}, {"$set": updated_log.dict()})
              print(f"Modified count: {result.modified_count}")
        elif tag_id:
            # Обновляем записи в логах по tag_id
            result = await logs_collection.update_many({"tag_id": tag_id}, {"$set": updated_log.dict()})

        if result.modified_count >= 1:
            return JSONResponse(content={"message": "Log(s) updated successfully"}, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"message": "Log(s) not found"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {str(e)}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
