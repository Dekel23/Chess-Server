from DB_manager import DB_Manager

class DB_User_Manager:
    def __init__(self, manager: DB_Manager, table_name: str) -> None:
        self.manager = manager
        self.table_name = table_name
        self.manager.create_table(self.table_name, 'name TEXT NOT NULL, password TEXT NOT NULL')
    
    def insert_user(self, name, password):
        self.manager.insert_data(self.table_name, (name, password))
    
    def remove_user(self, name, password):
        self.manager.remove_row(self.table_name, user_name = name, user_password = password)
    
    def user_exist(self, name, password):
        query = f'SELECT * FROM {self.table_name} WHERE name = ? AND password = ?'
        result = self.manager.execute_query(query, (name, password))
        return bool(result)
    
    def print_all_users(self):
        query = f'SELECT * FROM {self.table_name}'
        result = self.manager.execute_query(query)
        for row in result:
            print(row)
    
    def remove_all_users(self):
        query = f'DELETE FROM {self.table_name}'
        self.manager.execute_query(query)