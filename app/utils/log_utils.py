import os

from enum import Enum, auto
from ..models.collections_model import Task, Tag, Log
from db.settingsDB import SettingsDB

settingsDB = SettingsDB()

tags_collection = settingsDB.COLLECTION_TAGS
logs_collection = settingsDB.COLLECTION_LOGS

class TaskStatus(Enum):
    PENDING = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    CANCELLED = auto()
    FAILED = auto()
    PAUSED = auto()

async def create_log_entry(log_id: str, task_id: str, tag_id: str, rel_path_to_project: str) -> Log:
    # Определите статус лога, например, "IN_PROGRESS"
    log_status = TaskStatus.IN_PROGRESS.name

    # Создаем объект Log с использованием перечисления TaskStatus
    log = Log(
        id=log_id,
        task_id=task_id,
        tag_id=tag_id,
        status=log_status,
        name_doc="",
        path_to_doc="",
        progress_doc="",
        path_to_project=rel_path_to_project,
        progress_project=""
    )

    # Записываем объект Log в коллекцию logs
    await logs_collection.insert_one(log.dict())

    return log