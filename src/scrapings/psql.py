from typing import Union
import psycopg2

class Client:
    def __init__(self, host: str, port: int, user: str, database: str) -> Union[psycopg2.extensions.connection, psycopg2.extensions.cursor]:
        """
        Starts postgreSQL server and checks if conection is working properly.

        Returns:
            psycopg2.OperationalError: postgreSQL object to manage server connection
        """

        self.host, self.port , self.user, self.database = host, port, user, database
        self.connection, self.cursor = self.initialize_server()


    def initialize_server(self):
        try:
            connection = psycopg2.connect(
                host=self.host, port=self.port, user=self.user, database=self.database)

            connection.autocommit = True
            
            return (connection, connection.cursor())
        except psycopg2.OperationalError:
            e = """\n\nHere are a common ways to fix this problem:\n
            1. Check connectivity with your postgreSQL server verifing port availability\n
            2. If running on localhost, please install postgreSQL on your machine\n
            3. When running on a server, verify correct connecity between entities\n
            """

            print(e)
            raise   # If something goes wrong, ConnectionError is raised

    @property 
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, cursor):
        self._cursor = cursor
    
    @property
    def connection(self):
        return self._connection

    @connection.setter
    def connection(self, connection):
        self._connection = connection
        