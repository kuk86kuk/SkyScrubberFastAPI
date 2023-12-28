import os

from ..models.collections_model import Task, Tag, Log
from db.settingsDB import SettingsDB
from typing import Union, Optional
from pydantic import BaseModel, validator, Field, Json

settingsDB = SettingsDB()

tags_collection = settingsDB.COLLECTION_TAGS
logs_collection = settingsDB.COLLECTION_LOGS


async def create_log_entry(log_id: str, task_id: str, tag_id: str, rel_path_to_project: str, log_kwargs: Union[Json, dict]) -> Log:

    log = Log(
        id=log_id,
        task_id=task_id,
        tag_id=tag_id,
        path_to_project=rel_path_to_project,
        kwargs=log_kwargs,
    )

    await logs_collection.insert_one(log.dict())

    return log