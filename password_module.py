import bcrypt

class PasswordUtils:
    """
    A utility class for hashing and verifying passwords using bcrypt.
    """

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashes a password with a randomly generated salt.
        
        Args:
            password (str): The password to hash.
            
        Returns:
            str: The hashed password as a UTF-8 decodeable string
        """
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        return hashed_password.decode('utf-8')  # Convert bytes to string for storage

    @staticmethod
    def verify_password(entered_password: str, stored_hashed_password: str) -> bool:
        """
        Verifies if the entered password matches the stored hashed password.
        
        Args:
            entered_password (str): The password entered by the user
            stored_hashed_password (str): The hashed password stored as a string
            
        Returns:
            bool: True if password matches, False otherwise
        """
        entered_password_bytes = entered_password.encode('utf-8')
        stored_hash_bytes = stored_hashed_password.encode('utf-8')
        return bcrypt.checkpw(entered_password_bytes, stored_hash_bytes)