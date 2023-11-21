from pydantic import BaseModel



class Data(BaseModel):
    str1: str 
    str2: str 


class Path(BaseModel):
    path_to_directory: str
    file_processed: str