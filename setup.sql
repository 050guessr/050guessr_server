UPDATE mysql.user SET authentication_string = PASSWORD('siemsiem') WHERE User = 'root';
FLUSH PRIVILEGES;