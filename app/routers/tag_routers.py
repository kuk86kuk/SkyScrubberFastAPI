import os

from fastapi import FastAPI, HTTPException, APIRouter, status, BackgroundTasks
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from uuid import uuid4
from bson import ObjectId
from db.settingsDB import SettingsDB
from ..models.collections_model import Task, Tag, Log
from ..utils.log_utils import *
from ..utils.neuro_utils import *
router = APIRouter(prefix='/tags', tags=['tags'])

settingsDB = SettingsDB()
background_tasks = BackgroundTasks()

tags_collection = settingsDB.COLLECTION_TAGS
logs_collection = settingsDB.COLLECTION_LOGS

@router.post("/create_tag")
async def create_tag(tag: Tag):
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

@router.get("/get_tag/{tag_id}")
async def get_tag(tag_id: str):
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

@router.delete("/delete_tag/{tag_id}")
async def delete_tag(tag_id: str):
    try:
        result = await tags_collection.delete_one({"tag_id": tag_id})
        if result.deleted_count == 1:
            return JSONResponse(content={"message": "Tag deleted successfully"}, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"message": "Tag not found"}, status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JSONResponse(content={"message": f"Error: {str(e)}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.put("/update_tag_args/{tag_id}")
async def update_tag_args(tag_id: str, new_args: dict):
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