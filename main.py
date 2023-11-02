from fastapi import FastAPI
import os
 
app = FastAPI()
 
@app.get("/")
def read_root():
    return {"Hello": "World"}
 
@app.get("/items/{item_id}")
def read_item(item_id: int, query_param: str = None):
    return {"item_id": item_id, "query_param": query_param}





@app.get("/checks_all_directories/{name_directories}/{files_processed}")
def read_files_processing(files_processed, name_directories):
    directories, path = get_all_directories(name_directories + "/")
    processed, not_processed = checks_processed_directories( directories, path, files_processed)
    return {path: directories, "обработаные": processed, "не": not_processed }


def get_all_directories(path: str):
    '''
    Получает все дириктории по выбранному пути.
    Return directories_all: list, path: str
    '''
    directories_all = [f for f in os.listdir(path)]
    return directories_all, path


def checks_processed_directories(directories: list, path: str, files_processed: str):
    processed = []
    not_processed = []
    for direct in directories:
        direct_files = [f for f in os.listdir(path+direct)]
        flag = True
        for df in direct_files:
            if df == files_processed:
                flag = False
                not_processed.append(path+direct)
                break
        if flag:
           processed.append(path+direct)
    return processed, not_processed
