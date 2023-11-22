import asyncio
from motor.motor_asyncio import AsyncIOMotorClient



class SettingsDB():
    def __init__(self,
                  url='mongodb://localhost:27017', 
                  name_db='skyscrubber') -> None:
        
        # Создание клиента
        self.CLIENT = AsyncIOMotorClient(url) 

        # Получение базы данных
        self.DB = self.CLIENT[name_db]

        #Получение коллекции
        self.COLLECTION = self.DB[name_db]


if __name__ == "__main__":
    pass

