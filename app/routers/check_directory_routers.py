from fastapi import APIRouter
from app.models.db_model import Path
from app.main_defs import *



router = APIRouter(prefix='/checks_directory', tags=['checks_directory'])



# @router.get("/all")
# async def read_files_directories_processing(files_processed: Path): # изменить files_processed: Path!
#     '''
#     GET функция: Эта функция проверяет, массив директория на наличие обработаных дириктории нейронной сетью.
#     Args 
#         files_processed: Имя файла, который использовалась нейронная сеть для обработки данных.
#         name_directories: Имя директории, где использовалась нейронная сеть для обработки данных.
#     Returns:
#         Если name_directories == False:
#            Сообщение об ошибке, то что путь не верен или директории не существует.
#         list: {path: directories, "обработаные": processed, "не": not_processed }
#     '''
#     path = replace_underscore_with_slash(name_directories)
#     if not checks_exists_directories(path):
#         return f'Путь не верен или директории не существует {name_directories}  проверьте корректность вода'
#     directories, path = get_all_directories(path)
#     processed, not_processed = checks_processed_directories( directories, path, files_processed)
#     return {path: directories, "обработаные": processed, "не": not_processed }


# @router.get("/")
# async def read_files_directory_processing(files_processed: Path): # изменить files_processed: Path!
#     '''
#     GET функция: Эта функция проверяет, была ли выбранная директория обработана нейронной сетью.
#     Args 
#         files_processed: Имя файла, который использовалась нейронная сеть для обработки данных.
#         name_directories: Имя директории, где использовалась нейронная сеть для обработки данных.
#     Returns:
#         Если name_directories == False:
#             Сообщение об ошибке, то что путь не верен или директории не существует.
#         Если директория существует:
#             ______________________ (до писать)
#     '''
#     path = replace_underscore_with_slash(name_directories)
#     if not checks_exists_directories(path):
#         return f'Данной директории не существует {name_directories} проверьте корректность вода'
#     return get_directory(path, files_processed)
