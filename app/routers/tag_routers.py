import os
import shutil
from fastapi import FastAPI, HTTPException, APIRouter, status, BackgroundTasks, Depends
from fastapi.responses import JSONResponse
from uuid import uuid4
from bson import ObjectId
from app.models.collections_model import Task, Tag, Log
from ..utils.log_utils import *
from ..utils.neuro_utils import *
from db.settingsDB import settingsDB
from ..utils.auth_utils import decode_jwt_token
from celery.result import AsyncResult
from starlette import status
from celery import current_app 

router = APIRouter(prefix='/tags', tags=['tags'])
background_tasks = BackgroundTasks()

tasks_collection = settingsDB.COLLECTION_TASKS
tags_collection = settingsDB.COLLECTION_TAGS
logs_collection = settingsDB.COLLECTION_LOGS


@router.post("/")
async def create_tag(tag: Tag, current_user: dict = Depends(decode_jwt_token)):
    '''
    POST функция: Создает тег (tag).
    Parameters:
    - tag: Объект типа Tag, содержащий информацию о теге.
    Returns:
    JSONResponse с информацией об успешном создании тега или сообщением об ошибке.
    - В случае успешного создания: {"message": "Tag created successfully"} (статус 200 OK).
    - В случае ошибки: Сообщение об ошибке (статус 500 Internal Server Error).
    Описание:
    Эта функция обрабатывает POST-запросы для создания тега. Создается объект тега, добавляется в соответствующую коллекцию, и создается папка для тега в файловой системе. Затем возвращается JSONResponse с информацией об успешном создании тега. В случае ошибки возвращается соответствующее сообщение с статусом 500 Internal Server Error.
    '''
    try:
        created_tag = await tags_collection.insert_one(tag.dict())
        inserted_id = tag.tag_id 
        tag_folder_path = f"neuro/{tag.neuro_id}/{inserted_id}"
        os.makedirs(tag_folder_path, exist_ok=True)

        rel_path_to_project = f"neuro/{tag.neuro_id}/{tag.tag_id}"
        task_id = tag.tag_id
        run_neural_network.apply_async(args=[tag.neuro_id, tag.kwargs, rel_path_to_project], task_id=task_id)        
        return JSONResponse(status_code=status.HTTP_201_CREATED)
    except Exception as e:
        return JSONResponse(content={"message": f"Failed to create tag. Error: {str(e)}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get("/tag-status/{tag_id}")
async def get_tag_status(tag_id: str, current_user: dict = Depends(decode_jwt_token)):
    result = AsyncResult(tag_id, app=celery)
    task_status = result.state
    return {"task_id": tag_id, "status": task_status}
    
@router.get("/in_process")
async def get_tags_in_process(current_user: dict = Depends(decode_jwt_token)):
    active_tasks = celery.control.inspect().active()
    return {active_tasks}

@router.get("/progress/{tag_id}")
async def get_progress(tag_id: str, current_user: dict = Depends(decode_jwt_token)):
    try:
        log_entry = logs_collection.find_one({"tag_id": tag_id})

        if log_entry is None:
            raise HTTPException(status_code=404, detail=f"Log entry with tag_id {tag_id} not found")

        kwargs = log_entry.get("kwargs", {})
        save_dir = kwargs.get("save_dir", "save_image")  

        processed_files = len(os.listdir(os.path.join(save_dir)))
        unprocessed_files = len(os.listdir(os.path.join(log_entry["path_to_project"])))

        total_files = processed_files + unprocessed_files
        progress = (processed_files / total_files) * 100 if total_files > 0 else 0

        return JSONResponse(content={"progress": progress, "total_files": total_files})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{tag_id}")
async def get_tag(tag_id: str, current_user: dict = Depends(decode_jwt_token)):
    '''
    GET функция: Получает информацию о теге по его идентификатору.

    Parameters:
    - tag_id: Идентификатор тега, переданный в URL.

    Returns:
    JSONResponse с информацией о теге или сообщением об отсутствии тега.
    - В случае наличия тега: Информация о теге (статус 200 OK).
    - В случае отсутствия тега: {"message": "Tag not found"} (статус 404 Not Found).
    - В случае ошибки: Сообщение об ошибке (статус 500 Internal Server Error).

    Описание:
    Эта функция обрабатывает GET-запросы для получения информации о теге по его идентификатору. Поиск осуществляется в базе данных по заданному идентификатору тега. Если тег найден, его информация возвращается в виде JSONResponse. В противном случае возвращается сообщение о том, что тег не был найден. В случае ошибки также возвращается соответствующее сообщение.
    '''
    try:
        # Проекция для исключения поля _id
        projection = {"_id": 0}
        tag = await tags_collection.find_one({"tag_id": tag_id}, projection=projection)

        if tag:
            return JSONResponse(content=tag, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"message": "Tag not found"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {str(e)}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/{tag_id}")
async def delete_tag(tag_id: str, current_user: dict = Depends(decode_jwt_token)):
    try:
        # Поиск логов связанных с тегом
        logs = await logs_collection.find({"tag_id": tag_id}).to_list(length=None)

        if not logs:
            raise HTTPException(status_code=404, detail="Logs for tag not found")

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

            # Удаление записи в коллекции задач по task_id
            task_id = log.get("task_id")
            if task_id:
                await tasks_collection.delete_one({"task_id": task_id})

        # Затем удаляем сам тег
        result = await tags_collection.delete_one({"tag_id": tag_id})

        if result.deleted_count == 1:
            return JSONResponse(content={"message": "Tag and related data deleted successfully"}, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"message": "Tag not found"}, status_code=status.HTTP_404_NOT_FOUND)

    except HTTPException as he:
        raise he
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {str(e)}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/{tag_id}")
async def update_tag_args(tag_id: str, new_args: dict, current_user: dict = Depends(decode_jwt_token)):
    '''
    PUT функция: Обновляет аргументы тега по его идентификатору.

    Parameters:
    - tag_id: Идентификатор тега, переданный в URL.
    - new_args: Новые аргументы для обновления тега.

    Returns:
    JSONResponse с информацией об успешном обновлении аргументов тега или сообщением об отсутствии тега.
    - В случае успешного обновления: {"message": "Tag args updated successfully"} (статус 200 OK).
    - В случае отсутствия тега: {"message": "Tag not found"} (статус 404 Not Found).
    - В случае ошибки: Сообщение об ошибке (статус 500 Internal Server Error).

    Описание:
    Эта функция обрабатывает PUT-запросы для обновления аргументов тега по его идентификатору. Поиск тега в базе данных осуществляется по заданному идентификатору, и происходит обновление поля "args" новыми аргументами. Если тег найден и успешно обновлен, возвращается JSONResponse с сообщением об успешном обновлении. В случае, если тег не был найден, возвращается сообщение о его отсутствии.
    '''
    try:
        result = await tags_collection.update_one(
            {"tag_id": tag_id},
            {"$set": {"args": new_args}}
        )
        if result.modified_count == 1:
            return JSONResponse(content={"message": "Tag args updated successfully"}, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"message": "Tag not found"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {str(e)}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)