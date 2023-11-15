import os
from fastapi import FastAPI, Depends
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.models.task_model import TaskCreate, TaskDB

from app.models.database import get_database

app = FastAPI()

# Подключение к MongoDB
mongodb_uri = "mongodb://localhost:27017"
client = AsyncIOMotorClient(mongodb_uri)
db = client.get_database()

@app.post("/create_task/", response_model=TaskDB)
async def create_task(task: TaskCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    task_data = task.dict()
    collection = db.tasks
    result = await collection.insert_one(task_data)
    task_data["_id"] = result.inserted_id
    return TaskDB(**task_data)

@app.get("/get_tasks/", response_model=list[TaskDB])
async def get_tasks(db: AsyncIOMotorDatabase = Depends(get_database)):
    collection = db.tasks
    tasks = await collection.find().to_list(length=10)
    return tasks

@app.get("/checks_directories_all/{name_directories}/{files_processed}")
async def read_files_directories_processing(files_processed, name_directories):
    '''
    GET функция: Эта функция проверяет, массив директория на наличие обработаных дириктории нейронной сетью.
    Args 
        files_processed: Имя файла, который использовалась нейронная сеть для обработки данных.
        name_directories: Имя директории, где использовалась нейронная сеть для обработки данных.
    Returns:
        Если name_directories == False:
           Сообщение об ошибке, то что путь не верен или директории не существует.
        list: {path: directories, "обработаные": processed, "не": not_processed }
    '''
    path = replace_underscore_with_slash(name_directories)
    if not checks_exists_directories(path):
        return f'Путь не верен или директории не существует {name_directories}  проверьте корректность вода'
    directories, path = get_all_directories(path)
    processed, not_processed = checks_processed_directories( directories, path, files_processed)
    return {path: directories, "обработаные": processed, "не": not_processed }


async def get_all_directories(path: str):
    '''
    Получает всеx дириктории по выбранному пути.
    Return directories_all: list, path: str
    '''
    directories_all = [f for f in os.listdir(path)]
    return directories_all, path


async def checks_processed_directories(directories: list, path: str, files_processed: str):
    '''
    Функция проверяет выбранные директории на наличие файлов, обработанных нейронной сетью.
    Args:
        directories (list): Список директорий, которые нужно проверить.
        path (str): Путь к основной директории, в которой находятся выбранные директории.
        files_processed (sty): Имя файла, где использовалась нейронная сеть для обработки данных.
    :Returns: 
        list: processed - Список директорий, в которых файлы были обработаны нейронной сетью.
        list: not_processed -  Список директорий, в которых файлы не были обработаны нейронной сетью.
    '''
    processed = []
    not_processed = []
    for direct in directories:
        directory_files = [f for f in os.listdir(path+direct)]
        flag = True
        for df in directory_files:
            if df == files_processed:
                flag = False
                not_processed.append(path+direct)
                break
        if flag:
           processed.append(path+direct)
    return processed, not_processed


async def replace_underscore_with_slash(string):
    '''
    Заменяет все вхождения символа "_" на "/", и добавляет "/" в конец строки.
    Args:
        string (str): Исходная строка, в которой необходимо выполнить замену.
    Returns:
        str: Возвращает строку, в которой все символы "_" заменены на "/", и к ней добавлен символ "/" в конец.
    '''
    result_string = string.replace("_", "/") # Заменяем все вхождения "_" на "/"
    return result_string + '/' # Добавляем символ "/" в конец строки


async def checks_exists_directories(path: str):
    '''
    Проверяет существование директории по указанному пути.
    Args:
        path (str): Путь к директории, которую нужно проверить на существование.
    Returns:
        bool: Возвращает True, если директория существует, и False, если не существует.
    '''
    return True if os.path.exists(path) else False


@app.get("/checks_directory/{name_directories}/{files_processed}")
async def read_files_directory_processing(files_processed, name_directories):
    '''
    GET функция: Эта функция проверяет, была ли выбранная директория обработана нейронной сетью.
    Args 
        files_processed: Имя файла, который использовалась нейронная сеть для обработки данных.
        name_directories: Имя директории, где использовалась нейронная сеть для обработки данных.
    Returns:
        Если name_directories == False:
            Сообщение об ошибке, то что путь не верен или директории не существует.
        Если директория существует:
            ______________________ (до писать)
    '''
    path = replace_underscore_with_slash(name_directories)
    if not checks_exists_directories(path):
        return f'Данной директории не существует {name_directories} проверьте корректность вода'
    return get_directory(path, files_processed)


async def get_directory(path: str, files_processed: str):
    '''
    Проверяет наличие папки в указанном пути.
    Args:
        path (str): Путь к папке, которую нужно проверить на наличие.
        files_processed (str): Название файла или папки для сравнения с элементами в указанной директории.
    Returns:
        tuple:
            Возвращает кортеж, состоящий из двух элементов: (до писать)
            - Сообщение о состоянии директории (строка).
            - Флаг, указывающий на наличие директории (True - директория не обработана, False - директория уже обработана).
    '''
    directory_files = os.listdir(path)
    for df in directory_files:
        if df == files_processed:
            return 'Дириктория уже обработана', False
    return 'Дириктория не обработана', True 


@app.get("/database/info")
async def info_database():
    '''
    GET функция: Возвращает информацию о базе данных.
    Returns: 
        Строка с информацией о базе данных. методы и так далее (до писать)
    '''
    pass


@app.get("/database/get/{table}/{count}")
async def get_data_database(table, count=5):
    '''
    GET функция: Возвращает строки из базы данных, в количестве, указанном параметром count.
    Args 
        count, int: Количество строк для извлечения из базы данных. Значение по умолчанию: 5.

    Return: 
        list: Список строк из базы данных, соответствующих заданному количеству.
    '''
    pass


@app.delete("/database/delete/{table}/{id}")
async def delete_data_database(table, id):
    '''
    DELETE Функция: Удаляет строку из базы данных на основе указанной таблицы и идентификатора (ID).
    Args:
        table: Наименование таблицы, из которой нужно удалить строку.
        id: Идентификатор (ID) строки, которую необходимо удалить.

    Return: 
        Возвращает результат; 200 OK
    '''
    pass


@app.put("/database/put/{table}/{id}/{data}")
async def put_data_database(table, id, data):
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


@app.post("/database/post/{table}/{data}")
async def delete_data_database(table, data):
    '''
    POST Функция: Добавляет новую строку в указанную таблицу базы данных.
    Args:
        table: Наименование таблицы, в которую нужно добавить новую строку.
        data: Данные, которые необходимо добавить в виде строки или записи.
    Return: 
        Возвращает результат; 200 OK
    '''
    pass


@app.post('/processing_directory_all/{path_to_directories}/{file_processed}/{data}')
async def send_for_processing_directory_all(path_to_directories, file_processed, data):
    path = replace_underscore_with_slash(path_to_directories)
    if not checks_exists_directories(path):
        return f'Путь не верен или директории не существует {path}  проверьте корректность вода'


@app.post('/processing_directory/{path_to_directory}/{file_processed}/{data}')
async def send_for_processing_directory(path_to_directory, file_processed, data):
    '''
    GET Функция: Функция отправляет директорий на обработку нейросетью.
    Args:
        path_to_directory: Путь к директории, которую необходимо отправить на обработку.
        file_processed: Имя файла, который будет использоваться для обработки данных в директории.
         data: Данные или параметры, необходимые для процесса обработки.
    Return: 
        Возвращает результат; 200 OK
    '''
    path = replace_underscore_with_slash(path_to_directory)
    if not checks_exists_directories(path):
        return f'Путь не верен или директории не существует {path}  проверьте корректность вода'
    

@app.post('/processing_file/{name_file}/{data}')
async def processing_file(name_file, data):
    '''
    GET Функция: Функция отправляет файл на обработку нейросетью.
    Args:
        file_processed: Имя файла, который будет использоваться для обработки данных в директории.
        data: Данные или параметры, необходимые для процесса обработки.
    Return: 
        Возвращает результат; 200 OK
    '''
    pass
