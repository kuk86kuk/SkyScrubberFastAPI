import os

def get_all_directories(path: str):
    '''
    Получает все дириктории по выбранному пути.
    Return directories_all: list, path: str
    '''
    directories_all = [f for f in os.listdir(path)]
    return directories_all, path


def turn_neural_net(path: str):
    print("Нейроная сеть приведена в действия в дириктории " + path)
    


def checks_processed_directories(directories: list, path: str):
    processed = []
    not_processed = []
    for direct in directories:
        direct_files = [f for f in os.listdir(path+direct)]
        flag = True
        for df in direct_files:
            if df == 'files_processed':
                flag = False
                not_processed.append(path+direct)
                break
        if flag:
           processed.append(path+direct)



def replace_underscore_with_slash(input_string):
    # Заменяем все вхождения "_" на "/"
    result_string = input_string.replace("_", "/")
    return result_string



def get_directory(path: str):
    pass


print(os.path.exists('task/'))