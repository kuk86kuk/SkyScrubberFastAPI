import os
from fastapi import FastAPI, HTTPException, APIRouter, status, BackgroundTasks
from fastapi.responses import JSONResponse
from uuid import uuid4
from bson import ObjectId
from app.models.collections_model import Task, Tag, Log
from ..utils.log_utils import *
from ..utils.neuro_utils import *
from db.settingsDB import settingsDB


router = APIRouter(prefix='/tags', tags=['tags'])
background_tasks = BackgroundTasks()


tags_collection = settingsDB.COLLECTION_TAGS
logs_collection = settingsDB.COLLECTION_LOGS


@router.post("/")
async def create_tag(tag: Tag):
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
        inserted_id = created_tag.inserted_id 
        tag_folder_path = f"neuro/{tag.neuro_id}/{inserted_id}"
        os.makedirs(tag_folder_path, exist_ok=True)

        rel_path_to_project = f"neuro/{tag.neuro_id}/{tag.id}"
        #run_neural_network(tag.get("neuro_id"), tag.kwargs, rel_path_to_project)
        #background_tasks.add_task(run_neural_network, tag.get("neuro_id"), tag.kwargs, rel_path_to_project)
        return JSONResponse(content={"message": "Tag created successfully"}, status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(content={"message": f"Failed to create tag. Error: {str(e)}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/{tag_id}")
async def get_tag(tag_id: str):
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
async def delete_tag(tag_id: str):
    '''
    DELETE функция: Удаляет тег по его идентификатору.

    Parameters:
    - tag_id: Идентификатор тега, переданный в URL.

    Returns:
    JSONResponse с информацией об успешном удалении тега или сообщением об отсутствии тега.
    - В случае успешного удаления: {"message": "Tag deleted successfully"} (статус 200 OK).
    - В случае отсутствия тега: {"message": "Tag not found"} (статус 404 Not Found).
    - В случае ошибки: Сообщение об ошибке (статус 500 Internal Server Error).

    Описание:
    Эта функция обрабатывает DELETE-запросы для удаления тега по его идентификатору. Поиск тега в базе данных осуществляется по заданному идентификатору. Если тег найден и успешно удален, возвращается JSONResponse с сообщением об успешном удалении. В случае, если тег не был найден, возвращается сообщение о его отсутствии. В случае ошибки также возвращается соответствующее сообщение.
    '''
    try:
        result = await tags_collection.delete_one({"tag_id": tag_id})
        if result.deleted_count == 1:
            return JSONResponse(content={"message": "Tag deleted successfully"}, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"message": "Tag not found"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {str(e)}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/{tag_id}")
async def update_tag_args(tag_id: str, new_args: dict):
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