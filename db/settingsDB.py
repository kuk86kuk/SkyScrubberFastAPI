import asyncio
from motor.motor_asyncio import AsyncIOMotorClient



class SettingsDB():
    def __init__(self, url='mongodb://localhost:27017', db_name='taskmanagerdb') -> None:

        self.CLIENT = AsyncIOMotorClient(url) 

        self.DB = self.CLIENT[db_name]

        self.COLLECTION_TASKS = self.DB['tasks']
        self.COLLECTION_TAGS = self.DB['tags']
        self.COLLECTION_LOGS = self.DB['logs']      
        



if __name__ == "__main__":
    pass

