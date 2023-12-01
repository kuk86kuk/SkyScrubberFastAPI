import os
from db.database import DatabaseManager



DBM = DatabaseManager()



def get_all_directories(path: str):
    '''
    Получает всеx дириктории по выбранному пути.
    Return: 
        directories_all: list, path: str
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
