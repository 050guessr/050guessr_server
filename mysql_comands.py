# Teletubby code mode activated

import mysql.connector

class mysql_comands:
    def __init__(self, user="root", password="12345678"):
        """
        Initializes a MySQL connection and cursor.

        Parameters:
            user (str): MySQL username.
            password (str): MySQL password.
        """
        self.mydb = mysql.connector.connect(
            host="localhost", user=user, password=password
        )
        self.cursor = self.mydb.cursor(
            buffered=True
        )  # Set buffered=True to fetch all rows from server
        self.cursor.execute("SHOW DATABASES")

    def set_database(self, database_name):
        """
        Sets the active database to the specified database name.

        Parameters:
            database_name (str): The name of the database to set.

        Returns:
            None
        """
        self.mydb.database = database_name

    def create_database(self, database_name):
        """
        Creates a new database in MySQL.

        Parameters:
            database_name (str): The name of the database to be created.

        Returns:
            None
        """
        self.cursor.execute(f"CREATE DATABASE {database_name}")
        print(f"Database '{database_name}' created successfully!")
        self.mydb.commit()  # Commit after database creation

        # Fetch all remaining results from the cursor
        for result in self.cursor.stored_results():
            result.fetchall()

    def create_table(self, table_name, columns):
        """
        Creates a table in the MySQL database with the given table name and columns.

        Parameters:
            table_name (str): The name of the table to be created.
            columns (dict): A dictionary mapping column names to their data types.

        Returns:
            None
        """
        columns_with_types = []
        for col, dtype in columns.items():
            if dtype.lower() == "id":
                columns_with_types.append(f"{col} INT AUTO_INCREMENT PRIMARY KEY")
            else:
                columns_with_types.append(f"{col} {dtype}")
        create_table_query = (
            f"CREATE TABLE {table_name} ({', '.join(columns_with_types)});"
        )

        # Execute the query
        print(create_table_query)
        self.cursor.execute(create_table_query)

        # Fetch all remaining results from the cursor
        for result in self.cursor.stored_results():
            result.fetchall()

        print(f"Table '{table_name}' created successfully!")

    def insert_into_table(self, table_name, data):
        """
        Insert data into a MySQL table.

        Parameters:
            table_name (str): Name of the table to insert data into.
            data (dict): Dictionary of column names and their corresponding values.

        Returns:
            None
        """
        # Construct the INSERT INTO query
        columns = ", ".join(data.keys())
        values_placeholder = ", ".join(["%s"] * len(data))
        insert_query = (
            f"INSERT INTO {table_name} ({columns}) VALUES ({values_placeholder})"
        )

        # Execute the query
        self.cursor.execute(insert_query, list(data.values()))
        self.mydb.commit()

        # Fetch all remaining results from the cursor
        for result in self.cursor.stored_results():
            result.fetchall()

        print(f"Data inserted into '{table_name}' successfully!")


    def get_item(self, table_name, column_name, search_value):
        """
        A function to find an item in a specified table based on a search column and value.

        Parameters:
            table_name (str): The name of the table to search in.
            column_name (str): The column to search in.
            search_value (any): The value to search for in the specified column.

        Returns:
            the item
        """
        # Construct the SQL query to select all rows from the table
        # where the specified column matches the search value
        query = f"SELECT * FROM {table_name} WHERE {column_name} = %s"

        # Execute the query with the search value as a parameter
        self.cursor.execute(query, (search_value,))

        # Fetch the first row that matches the search criteria
        # If no rows match, None is returned
        result = self.cursor.fetchone()

        return result


    def edit_item(
        self, table_name, column_name, new_value, search_column, search_value
    ):
        """
        A function to edit an item in a specified table by updating a specific column with a new value based on a search column and value.

        Parameters:
            table_name (str): The name of the table to edit.
            column_name (str): The column to update with the new value.
            new_value (any): The new value to be set in the specified column.
            search_column (str): The column to search for the specified value.
            search_value (any): The value to search for in the search column.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        query = f"UPDATE {table_name} SET {column_name} = %s WHERE {search_column} = %s"

        # Execute the query
        self.cursor.execute(query, (new_value, search_value))

        # Commit the changes
        self.mydb.commit()

        if self.cursor.rowcount > 0:
            return True  # Return True if the update was successful
        else:
            return False  # Return False if no rows were updated
        
    def get_all_items_sorted(self, table_name, column_name, descending=False):
        """
        Retrieves all items from a specified table sorted by a specific column.

        Args:
            table_name (str): The name of the table.
            column_name (str): The column to sort by.
            descending (bool): Whether to sort in descending order. Default is False.

        Returns:
            list: A list of sorted items from the table.
        """
        order = "DESC" if descending else "ASC"
        query = f"SELECT * FROM {table_name} ORDER BY {column_name} {order}"
        self.cursor.execute(query)
        columns = [column[0] for column in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

