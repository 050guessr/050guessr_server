import bcrypt

class PasswordUtils:
    """
    A utility class for hashing and verifying passwords using bcrypt.
    """

    def __init__(self):
        """
        Initialize the PasswordUtils class.
        No need for specific initialization, but it could be extended in the future.
        """
        pass

    def hash_password(password: str) -> bytes:
        """
        Hashes a password with a randomly generated salt.

        Args:
            password (str): The password to hash.

        Returns:
            bytes: The hashed password including the salt.
        """
        # Convert the password to bytes
        password_bytes = password.encode('utf-8')
        
        # Generate a random salt
        salt = bcrypt.gensalt()
        
        # Hash the password with the salt
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        
        return hashed_password

    def verify_password( entered_password: str, stored_hashed_password: str) -> bool:
        """
        Verifies if the entered password matches the stored hashed password.

        Args:
            entered_password (str): The password entered by the user.
            stored_hashed_password (str): The hashed password stored in the database.

        Returns:
            bool: True if the password is correct, False otherwise.
        """
        # Convert the entered password to bytes
        entered_password_bytes = entered_password.encode('utf-8')

        # Convert the stored hashed password back to bytes (it might have been stored as a string)
        stored_hashed_password_bytes = stored_hashed_password.encode('utf-8')

        # Check if the entered password matches the stored hashed password
        return bcrypt.checkpw(entered_password_bytes, stored_hashed_password_bytes)