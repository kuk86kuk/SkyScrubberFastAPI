from fastapi import FastAPI
import os

from database.database import get_data


app = FastAPI()


@app.get("/checks_all_directories/{name_directories}/{files_processed}")
def read_files_directories_processing(files_processed, name_directories):
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


def get_all_directories(path: str):
    '''
    Получает всеx дириктории по выбранному пути.
    Return directories_all: list, path: str
    '''
    directories_all = [f for f in os.listdir(path)]
    return directories_all, path


def checks_processed_directories(directories: list, path: str, files_processed: str):
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


def replace_underscore_with_slash(string):
    '''
    Заменяет все вхождения символа "_" на "/", и добавляет "/" в конец строки.
    Args:
        string (str): Исходная строка, в которой необходимо выполнить замену.
    Returns:
        str: Возвращает строку, в которой все символы "_" заменены на "/", и к ней добавлен символ "/" в конец.
    '''
    result_string = string.replace("_", "/") # Заменяем все вхождения "_" на "/"
    return result_string + '/' # Добавляем символ "/" в конец строки


def checks_exists_directories(path: str):
    '''
    Проверяет существование директории по указанному пути.
    Args:
        path (str): Путь к директории, которую нужно проверить на существование.
    Returns:
        bool: Возвращает True, если директория существует, и False, если не существует.
    '''
    return True if os.path.exists(path) else False


@app.get("/checks_directory/{name_directories}/{files_processed}")
def read_files_directory_processing(files_processed, name_directories):
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


def get_directory(path: str, files_processed: str):
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


@app.get("/database/")
def info_database():
    '''
    GET функция: Возвращает информацию о базе данных.
    Returns: 
        Строка с информацией о базе данных. (до писать)
    '''
    return 'информация о базе данных'


@app.get("/database/get/{count}")
def get_data_database(count=5):
    '''
    GET функция: Возвращает строки из базы данных, в количестве, указанном параметром count.
    Returns 
        count, int: Количество строк для извлечения из базы данных. Значение по умолчанию: 5.

    Return: 
        list: Список строк из базы данных, соответствующих заданному количеству.
    '''
    if int(count)<= 0:
        return 'отрицательное количество '
    data = get_data(count)
    return data

