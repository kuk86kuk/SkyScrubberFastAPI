from fastapi import APIRouter
from app.routers.models.models_processing import Data, Path
from app.models.task_model import tasks
from app.routers.main_defs import *



router = APIRouter(prefix='/processing_directory', tags=['processing_directory'])



@router.post('/all/')
async def send_for_processing_directory(FileProcessed: Path, data: Data): # FileProcessed: Path,  изменить!!!
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
    print(path)

    if not checks_exists_directories(path):
        return f'Путь не верен или директории не существует {path}  проверьте корректность вода'
    directories, path = get_all_directories(path)
    
    arr_json = []
    for dirictory in directories:
        path_to_dir = path + dirictory
        json = tasks(path_to_dir, data)
        arr_json.append(json)
    
    DBM.do_insert_arr_in_db(arr_json)
    return 200
    
    

@router.post('/')
async def processing_file(path_to_name_file: Path, data: Data): # path_to_name_file: Path,  изменить!!!
    '''
    GET Функция: Функция отправляет файл на обработку нейросетью.
    Args:
        file_processed: Имя файла, который будет использоваться для обработки данных в директории.
        data: Данные или параметры, необходимые для процесса обработки.
    Return: 
        Возвращает результат; 200 OK
    '''
    path = replace_underscore_with_slash(path_to_name_file)

    if not checks_exists_directories(path):
        return {f'Путь не верен или директории не существует {path}  проверьте корректность вода'}
    
    json = tasks(path, data)
    DBM.do_insert_in_db(json)
    return 200