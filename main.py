from fastapi import FastAPI
import os



app = FastAPI()


@app.get("/checks_all_directories/{name_directories}/{files_processed}")
def read_files_directories_processing(files_processed, name_directories):
    path = replace_underscore_with_slash(name_directories)
    if not checks_exists_directories(path):
        return f'Данной директории не существует {name_directories} проверьте корректность вода'
    directories, path = get_all_directories(path)
    processed, not_processed = checks_processed_directories( directories, path, files_processed)
    return {path: directories, "обработаные": processed, "не": not_processed }


def get_all_directories(path: str):
    '''
    Получает всеx дириктории по выбранному пути.
    Return directories_all: list, path: str
    '''
    directories_all = [f for f in os.listdir(path)]
    return directories_all, path


def checks_processed_directories(directories: list, path: str, files_processed: str):
    '''
    Функция провреярет выбранные дириктории на наличие, что их уже обрабатывала нейронка
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


def replace_underscore_with_slash(string):
    # Заменяем все вхождения "_" на "/" и добовляет на конец /
    result_string = string.replace("_", "/")
    return result_string + '/'


def checks_exists_directories(path: str):
    return True if os.path.exists(path) else False


@app.get("/checks_directory/{name_directories}/{files_processed}")
def read_files_directory_processing(files_processed, name_directories):
    path = replace_underscore_with_slash(name_directories)
    if not checks_exists_directories(path):
        return f'Данной директории не существует {name_directories} проверьте корректность вода'
    return get_directory(path, files_processed)


def get_directory(path: str, files_processed: str):
    directory_files = os.listdir(path)
    for df in directory_files:
        if df == files_processed:
            return 'Дириктория уже обработана', False
    return 'Дириктория не обработана', True 