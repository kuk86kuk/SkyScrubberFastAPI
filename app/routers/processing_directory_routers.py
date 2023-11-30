from fastapi import APIRouter
from app.models.db_model import Data, Path
from app.models.collections_model import tasks
from app.main_defs import *



router = APIRouter(prefix='/processing_directory', tags=['processing_directory'])



@router.post('/all/')
async def send_for_processing_directory(path_data: Path, data: Data):
    '''
    Функция POST: Отправляет директорию на обработку нейросетью.
    Аргументы:
        path_data: JSON-объект, содержащий атрибуты "path_to_directory" и "file_processed".
        data: Данные или параметры, необходимые для процесса обработки.
    Возвращает: 
        Результат; 200 OK
    '''  
    path = replace_underscore_with_slash(path_data.path_to_directory)
    print(path)

    if not checks_exists_directories(path):
        return f'Путь неверен или директория не существует {path}. Пожалуйста, проверьте правильность ввода.'
    
    directories, path = get_all_directories(path)
    
    arr_json = []
    for directory in directories:
        path_to_dir = path + directory
        json_result = tasks(path_to_dir, data)
        arr_json.append(json_result)
    
    DBM.do_insert_arr_in_db(arr_json)
    return 200

@router.post('/')
async def processing_file(file_data: Path, data: Data):
    '''
    Функция POST: Отправляет файл на обработку нейросетью.
    Аргументы:
        file_data: JSON-объект, содержащий атрибуты "path_to_directory" и "file_processed".
        data: Данные или параметры, необходимые для процесса обработки.
    Возвращает: 
        Результат; 200 OK
    '''
    path = replace_underscore_with_slash(file_data.path_to_directory)

    if not checks_exists_directories(path):
        return f'Путь неверен или директория не существует {path}. Пожалуйста, проверьте правильность ввода.'
    
    json_result = tasks(path, data)
    DBM.do_insert_in_db(json_result)
    return 200