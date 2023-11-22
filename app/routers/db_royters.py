from fastapi import APIRouter
from app.routers.models.models_db import DataDB
from app.routers.main_defs import *



router = APIRouter(prefix='/database', tags=['database'])



@router.get("/info")
async def info_database():
    '''
    GET функция: Возвращает информацию о базе данных.
    Returns: 
        Строка с информацией о базе данных. методы и так далее (до писать)
    '''
    pass


@router.get("/get")
async def get_data_database(collection: DataDB):
    '''
    GET функция: Возвращает строки из базы данных, в количестве, указанном параметром count.
    Args 
        count, int: Количество строк для извлечения из базы данных. Значение по умолчанию: 5.

    Return: 
        list: Список строк из базы данных, соответствующих заданному количеству.
    '''
    if count.isdigit():
        return {'count, должен быть числом'}

@router.post("/post")
async def post_data_database(collection: DataDB):
    '''
    DELETE Функция: Удаляет строку из базы данных на основе указанной таблицы и идентификатора (ID).
    Args:
        table: Наименование таблицы, из которой нужно удалить строку.
        id: Идентификатор (ID) строки, которую необходимо удалить.

    Return: 
        Возвращает результат; 200 OK
    '''
    pass

@router.put("/put")
async def put_data_database(collection: DataDB):
    '''
    PUT Функция: Обновляет строку в определенной таблице базы данных на основе указанного идентификатора (ID).
    Args:
        table: Наименование таблицы, в которой нужно обновить строку.
        id: Идентификатор (ID) строки, которую необходимо обновить.
        data: Новые данные, которыми нужно обновить строку.
    Return: 
        Возвращает результат; 200 OK
    '''
    pass

@router.delete("/delete")
async def delete_data_database(collection: DataDB):
    '''
    DELETE Функция: Удаляет строку в указанную таблицу базы данных.
    Args:
        table: Наименование таблицы, в которую нужно добавить новую строку.
        data: Данные, которые необходимо добавить в виде строки или записи.
    Return: 
        Возвращает результат; 200 OK
    '''
    DBM.delete_line_db(collection, id) # допиасать, как удаялеть будет
    return 200