import asyncio
from motor.motor_asyncio import AsyncIOMotorClient



class SettingsDB():
    def __init__(self, url='mongodb://localhost:27017', db_name='taskmanagerdb') -> None:
        # Создание клиента
        self.CLIENT = AsyncIOMotorClient(url) 

        # Получение базы данных
        self.DB = self.CLIENT[db_name]

        # Получение коллекции
        self.COLLECTION_TASKS = self.DB['tasks']
        
        self.COLLECTION_TAGS = self.DB['tags']
        
        self.COLLECTION_LOGS = self.DB['logs']      
        



if __name__ == "__main__":
    pass

