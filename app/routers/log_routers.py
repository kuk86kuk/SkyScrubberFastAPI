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
import logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix='/logs', tags=['logs'])

settingsDB = SettingsDB()

logs_collection = settingsDB.COLLECTION_LOGS

from fastapi import HTTPException, Query

@router.get("/")
async def get_logs(task_id: str = Query(None), tag_id: str = Query(None)):
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