import datetime
from pydantic import BaseModel, validator, Field, Json
from typing import Union, Optional


class Task(BaseModel):
    task_id: str
    neuro_id: str
    kwargs:Union[Json, dict] 
    
class Tag(BaseModel):
    tag_id: Optional[str] = None
    task_id: Optional[str] = None
    neuro_id: str #Т.е. какая нейронка запущена
    kwargs:Union[Json, dict] 

class Log(BaseModel):
    id: str
    task_id: str
    tag_id: Optional[str] = None
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
     
