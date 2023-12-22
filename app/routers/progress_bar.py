import os
from fastapi import APIRouter
from db.settingsDB import settingsDB



router = APIRouter(prefix='/progress_bar', tags=['progress_bar'])


@router.get('/')
async def progress_bar():
    '''
    Эта функция извлекает последнюю запись журнала из базы данных 
    настроек и вычисляет ход выполнения задачи
    Затем она возвращает словарь с информацией о ходе выполнения, 
    обрабатываемых каталогах, статусе, идентификаторе задачи, идентификаторе тега и идентификаторе журнала.
    '''
    json_log = await settingsDB.COLLECTION_LOGS.find_one({}, sort=[("register_date", -1)])
    path_to_directories_len = len(os.listdir(json_log['path_to_directories']))
    path_to_project_len = len(os.listdir(json_log['path_to_project']))
    percentage_completion = '0%' if path_to_project_len == 0 else str(round((path_to_directories_len / path_to_project_len) * 100)) + '%'
    return {'Прогрес обработки состовляет': percentage_completion,
        'Обработка дириктори': json_log['path_to_directories'],
        'статус': json_log['status'],
        'task_id': json_log['task_id'],
        "tag_id": json_log['tag_id'],
        "log_id": json_log['id']}

