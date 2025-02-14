import sqlite3
from threading import Lock

class sqlite_commands:
    def __init__(self, database_name="main.db", user=None, password=None):
        self.database_name = database_name
        self.lock = Lock()  # Add lock for thread safety
        if user or password:
            print("warning: using user and password is deprecated")

    def _execute(self, query, params=(), commit=True):
        """Generic execute method with connection handling"""
        with self.lock, sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if commit:
                conn.commit()
            return cursor

    def create_database(self, database_name):
        """Maintained for compatibility (SQLite auto-creates)"""
        print(f"Using SQLite database file: {database_name}")
        print("warning: this function is deprecated")

    def set_database(self, database_name):
        """Switch database by changing the filename"""
        self.database_name = database_name

    def create_table(self, table_name, columns):
        columns_with_types = []
        for col, dtype in columns.items():
            if dtype.lower() == "id":
                columns_with_types.append(f"{col} INTEGER PRIMARY KEY AUTOINCREMENT")
            else:
                columns_with_types.append(f"{col} {dtype}")
        
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns_with_types)})"
        self._execute(query)

    def insert_into_table(self, table_name, data):
        columns = ", ".join(data.keys())
        values_placeholder = ", ".join(["?"] * len(data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values_placeholder})"
        self._execute(query, list(data.values()))
        print(f"Data inserted into '{table_name}' successfully!")

    def get_item(self, table_name, column_name, search_value):
        """
        Retrieves a single row from a table based on a column value.
        
        Args:
            table_name (str): The name of the table
            column_name (str): The name of the column to search
            search_value (str): The value to search for
            
        Returns:
            dict: A single row as a dictionary
        """
        query = f"SELECT * FROM {table_name} WHERE {column_name} = ?"
        cursor = self._execute(query, (search_value,), commit=False)
        return cursor.fetchone()

    def edit_item(self, table_name, column_name, new_value, search_column, search_value):
        query = f"UPDATE {table_name} SET {column_name} = ? WHERE {search_column} = ?"
        cursor = self._execute(query, (new_value, search_value))
        return cursor.rowcount > 0

    def get_all_items_sorted(self, table_name, column_name, descending=False):
        order = "DESC" if descending else "ASC"
        query = f"SELECT * FROM {table_name} ORDER BY {column_name} {order}"
        cursor = self._execute(query, commit=False)
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def add_column(self, table_name, column_name, column_type):
        try:
            query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"
            self._execute(query)
            print(f"Column '{column_name}' added to table '{table_name}' successfully!")
        except sqlite3.Error as err:
            print(f"Error: {err}")