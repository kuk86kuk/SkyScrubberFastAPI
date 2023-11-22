from .settings.settingsDB import SettingsDB


class DatabaseManager(): 
    def __init__(self) -> None:
        self.SETTINGSDB = SettingsDB()


    def do_insert_in_db(self, json):
        '''
        Метод, который встовляет выбранный json в базу данных
        Args:
            db: база данных
            json: json обект который для записи в базу данных
        Return: 
            pass (дописать)
        '''
        self.SETTINGSDB.DB.test.insert_one(json)
        self.SETTINGSDB.CLIENT.get_io_loop()
        return 200
    
    
    def do_insert_arr_db(self, arr_json):
        '''
        Метод, который встовляет массив json в базу данных
        Args:
            db: база данных
            arr_json: массив обектов для записи в базу данных
        Return: 
            pass (дописать)
        '''
        self.SETTINGSDB.DB.test.insert_many(arr_json)
        self.SETTINGSDB.CLIENT.get_io_loop()
        return 200
    

    def delete_line_db(self, collection, id):
        '''
        Метод, удаляет json по выбраному id
        Args:
            collection: база данных
            id: id json
        Return: 
            pass (дописать)
        '''
        document_to_delete = {'args': id}
        self.SETTINGSDB.DB[collection].delete_one(document_to_delete)
        self.SETTINGSDB.CLIENT.get_io_loop()
        return 200
    
    
    def remove_lines_arr_db(self, collection, arr_id):
        '''
        Метод, удаляет массив json по выбраномым id
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

