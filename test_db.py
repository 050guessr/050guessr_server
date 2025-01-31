from mysql_comands import *
import os


def main():
    # Remove existing test database to start fresh
    if os.path.exists("test.db"):
        os.remove("test.db")
    
    db = sqlite_commands("test.db")
    
    # Test create_table
    print("Testing create_table...")
    test_columns = {'id': 'id', 'name': 'TEXT', 'age': 'INTEGER'}
    db.create_table('users', test_columns)
    # Verify table creation
    cursor = db._execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'", commit=False)
    assert cursor.fetchone() is not None, "Table creation failed"
    print("create_table test passed!\n")
    
    # Test insert_into_table
    print("Testing insert_into_table...")
    db.insert_into_table('users', {'name': 'John Doe', 'age': 30})
    db.insert_into_table('users', {'name': 'Jane Smith', 'age': 25})
    # Verify inserts
    cursor = db._execute("SELECT * FROM users", commit=False)
    results = cursor.fetchall()
    assert len(results) == 2, "Insert count mismatch"
    print("insert_into_table test passed!\n")
    
    # Test get_item
    print("Testing get_item...")
    john = db.get_item('users', 'name', 'John Doe')
    assert john[2] == 30, "Data retrieval failed"
    non_existent = db.get_item('users', 'name', 'Ghost')
    assert non_existent is None, "Non-existent item check failed"
    print("get_item test passed!\n")
    
    # Test edit_item
    print("Testing edit_item...")
    success = db.edit_item('users', 'age', 31, 'name', 'John Doe')
    assert success, "Update operation failed"
    updated_john = db.get_item('users', 'name', 'John Doe')
    assert updated_john[2] == 31, "Data update failed"
    print("edit_item test passed!\n")
    
    # Test add_column
    print("Testing add_column...")
    db.add_column('users', 'email', 'TEXT')
    # Verify column addition
    cursor = db._execute("PRAGMA table_info(users)", commit=False)
    columns = [col[1] for col in cursor.fetchall()]
    assert 'email' in columns, "New column not found"
    # Test insert with new column
    db.insert_into_table('users', {'name': 'Alice', 'age': 28, 'email': 'alice@test.com'})
    alice = db.get_item('users', 'name', 'Alice')
    assert alice[3] == 'alice@test.com', "New column data mismatch"
    print("add_column test passed!\n")
    
    # Test get_all_items_sorted
    print("Testing get_all_items_sorted...")
    # Ascending test
    ascending = db.get_all_items_sorted('users', 'age')
    assert [user['age'] for user in ascending] == [25, 28, 31], "Ascending sort failed"
    # Descending test
    descending = db.get_all_items_sorted('users', 'age', descending=True)
    assert [user['age'] for user in descending] == [31, 28, 25], "Descending sort failed"
    print("get_all_items_sorted test passed!\n")
    
    print("All tests completed successfully!")

if __name__ == "__main__":
    main()