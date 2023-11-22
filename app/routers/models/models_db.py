from pydantic import BaseModel


class DataDB(BaseModel):
    name_collection: str
    id: str
    data: dict