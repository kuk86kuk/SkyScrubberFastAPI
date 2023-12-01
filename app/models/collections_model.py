import datetime
from pydantic import BaseModel, validator, Field, Json
from typing import Union, Optional


class Task(BaseModel):
    neuro_id: str
    args:Union[Json, dict] 
    
class Tag(BaseModel):
    task_id: Optional[str] = None
    neuro_id: str #Т.е. какая нейронка запущена
    args:Union[Json, dict] 

class Log(BaseModel):
    id: str
    status: str
    name_doc: str #doc - Это фотка в формате .tif
    path_to_doc: str
    progress_doc: str
    path_to_project: str
    progress_project: str
    register_date: datetime.datetime = Field(default_factory=datetime.datetime.now)

    class Config:
        arbitrary_types_allowed = True
    
    @validator("register_date", pre=True, always=True)
    def set_default_time(cls, value):
        return value if value is not None else datetime.datetime.now() 
     

def logs(docs, tag_id):
    json = {
        "id": docs,
        "task": tag_id,
        'register_datatime': datetime.datetime.now()
    }
    return json



def tags(tag, name, process):
    json = {
        "tag": tag,
        "name": name,
        "process": process,
        'time': datetime.datetime.now()
    }
    return json



def tasks(path, args):
    json = {
        "path": path,
        "args": args
    }
    return json

