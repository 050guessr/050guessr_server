from mysql_comands import *

database = mysql_comands()
database.create_database("test3")
database.set_database("test3")
database.create_table("users", {"id": "INT AUTO_INCREMENT PRIMARY KEY", "username": "VARCHAR(255)", "password": "VARCHAR(255)", "user_score": "INT", "user_rank": "INT", "user_key": "VARCHAR(255)"})
database.insert_into_table("users", {"username": "siem", "password": "test1", "user_score": 0, "user_rank": 0, "user_key": "YUdWdWEwRnVaSE5wWlcwPQ=="})
#test the check_and_get_item function
print(database.get_item("users", "user_key", "YUdWdWEwRnVaSE5wWlcwPQ==")[1])