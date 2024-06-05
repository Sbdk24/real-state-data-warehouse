from typing import Union
import psycopg2

def get_psql_client(host: str, port: int, user: str, database: str) -> Union[psycopg2.extensions.connection, psycopg2.extensions.cursor]:
    """
    Starts postgreSQL server and checks if conection is working properly.

    Returns:
        psycopg2.OperationalError: postgreSQL object to manage server connection
    """

    try:
        connection = psycopg2.connect(
            host=host, port=port, user=user, database=database)

        connection.autocommit = False
        
        return (connection, connection.cursor())
    except psycopg2.OperationalError:
        e = """\n\nHere are a common ways to fix this problem:\n
        1. Check connectivity with your postgreSQL server verifing port availability\n
        2. If running on localhost, please install postgreSQL on your machine\n
        3. When running on a server, verify correct connecity between entities\n
        """

        print(e)
        raise   # If something goes wrong, ConnectionError is raised