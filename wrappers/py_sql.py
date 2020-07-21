from mysql import connector


class PySQL(object):
    def __init__(self, host, port, database, user, password, query='', params=None):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.query = query
        self.params = params
        self.db_connection = None
        self.db_cursor = None

    def set_db_connection(self):
        try:
            self.db_connection = connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                passwd=self.password
            )
        except Exception as e:
            raise e

    def execute_query(self):
        self.set_db_connection()
        try:
            self.db_cursor = self.db_connection.cursor(dictionary=True)
            if self.params:
                self.db_cursor.execute(self.query, self.params)
            else:
                self.db_cursor.execute(self.query)
        except Exception as e:
            raise e

    def fetch_one(self):
        self.execute_query()
        try:
            result = self.db_cursor.fetchone()
            if result:
                return result
            else:
                return {}
        except Exception as e:
            raise e

    def fetch_all(self):
        self.execute_query()
        try:
            result = self.db_cursor.fetchall()
            if result:
                return result
            else:
                return []
        except Exception as e:
            raise e

    def save_changes(self):
        self.execute_query()
        self.db_connection.commit()
        self.db_connection.close()