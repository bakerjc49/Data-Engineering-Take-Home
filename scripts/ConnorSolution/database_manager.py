import psycopg2


# Class to control database operations
class DatabaseManager:
    connection = None
    cursor = None

    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database

    # Sets up a connection to the supplied database
    def setup_connection(self):
        try:
            self.connection = psycopg2.connect(user=self.user,
                                               password=self.password,
                                               host=self.host,
                                               port=self.port,
                                               database=self.database)
            self.cursor = self.connection.cursor()
        except Exception as error:
            print("Failed to connect to database.", error)

    # Closes the connection to the database if it exists
    def close_connection(self):
        if self.connection is None:
            return

        # Close the cursor and connection
        self.cursor.close()
        self.cursor = None
        self.connection.close()
        self.connection = None

    # Inserts records based off a query into the database
    def execute_query(self, query, records):
        if self.cursor is None:
            return

        try:
            self.cursor.execute(query, (records,))
            self.connection.commit()
        except Exception as error:
            print("Failed to insert data to database.", error)
