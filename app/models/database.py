from settings.settings import SETTINGSDB
import asyncio
from task_model import document1



class DatabaseManager(): 
    def do_insert_in_db(self, json):
        '''
        Cтатический метод, который встовляет выбранный json в базу данных
        Args:
            db: база данных
            json: json обект который для записи в базу данных
        Return: 
            pass (дописать)
        '''
        SETTINGSDB.DB.test.insert_one(json)
        SETTINGSDB.CLIENT.get_io_loop()
        return 200
    
    
    def do_insert_arr_in_db(self, arr_json):
        '''
        Cтатический метод, который встовляет массив json в базу данных
        Args:
            db: база данных
            arr_json: массив обектов для записи в базу данных
        Return: 
            pass (дописать)
        '''
        SETTINGSDB.DB.test.insert_many(arr_json)
        SETTINGSDB.CLIENT.get_io_loop()
        return 200
    

    def remove_line_db(self, db, id):
        '''
        Cтатический метод, который удаляет json по выбраному id
        Args:
            db: база данных
            id: id json
        Return: 
            pass (дописать)
        '''
        pass
    

    
    def remove_lines_arr_db(self, db, arr_id):
        '''
        Cтатический метод, который удаляет массив json по выбраномым id
        Args:
            db: база данных
            arr_id: arr id json
        Return: 
            pass (дописать)
        '''
        pass


    def put_line_db(self, db, id, json):
        '''
        Cтатический метод, который изменяет json по выбраному id
        Args:
            db: база данных
            id: id json
        Return: 
            pass (дописать)
        '''
        pass


    def parser_in_json(self, json):
        '''
        есть сомнения нужен ли 
        Метод класса, который парсет словарь в json
        Args:
            db: база данных
            id: id json
        Return: 
            pass (дописать)
        '''
        return json


    def parser_from_json(self, json):
        '''
        есть сомнения нужен ли 
        Метод класса, который парсет json в словарь
        Args:
            db: база данных
            id: id json
        Return: 
            pass (дописать)
        '''
        return json


DBM = DatabaseManager()
docu = document1(1, 'сделал тото')
DBM.do_insert_in_db(docu)