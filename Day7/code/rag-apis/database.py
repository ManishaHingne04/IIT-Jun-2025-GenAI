import mysql.connector

class Database:
    def __init__(self):
        # create a connection to the database
        self.__connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="root",
            database="rag_db",
            port=3306
        )

    def __del__(self):
        # close the connection if it is open
        if self.__connection.is_connected():
            self.__connection.close()

    def execute_query(self, query):
        # get the cursor
        cursor = self.__connection.cursor()

        # execute the query
        cursor.execute(query)

        # get the result
        result = cursor.fetchall()

        # close the cursor
        cursor.close()

        return result