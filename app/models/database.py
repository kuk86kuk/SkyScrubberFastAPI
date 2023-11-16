from settings.settings import SETTINGSDB
import asyncio

class DatabaseManager():

    @staticmethod
    def do_insert_in_db(db, json):
        '''
        Cтатический метод, который встовляет выбранный json в базу данных
        Args:
            db: база данных
            json: json обект который для записи в базу данных
        Return: 
            pass (дописать)
        '''
        instance = DatabaseManager()
        pass
    

    @staticmethod
    def do_insert_arr_in_db(db, arr_json):
        '''
        Cтатический метод, который встовляет массив json в базу данных
        Args:
            db: база данных
            arr_json: массив обектов для записи в базу данных
        Return: 
            pass (дописать)
        '''
        instance = DatabaseManager()
        pass
    

    @staticmethod
    def remove_line_db(db, id):
        '''
        Cтатический метод, который удаляет json по выбраному id
        Args:
            db: база данных
            id: id json
        Return: 
            pass (дописать)
        '''
        instance = DatabaseManager()
        pass
    

    @staticmethod
    def remove_lines_arr_db(db, arr_id):
        '''
        Cтатический метод, который удаляет массив json по выбраномым id
        Args:
            db: база данных
            arr_id: arr id json
        Return: 
            pass (дописать)
        '''
        instance = DatabaseManager()
        pass


    @staticmethod
    def put_line_db(db, id, json):
        '''
        Cтатический метод, который изменяет json по выбраному id
        Args:
            db: база данных
            id: id json
        Return: 
            pass (дописать)
        '''
        instance = DatabaseManager()
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


DatabaseManager.do_insert_db(123)