import psycopg2


class DatabaseConnector:
    def __init__(self, config_details):
        self.config = config_details.database
        self.conn = None

    def connect(self):
        if self.conn is None:
            self.conn = psycopg2.connect(
                dbname=self.config.db_name,
                user=self.config.user,
                password=self.config.password,
                host=self.config.host,
                port=self.config.port
            )

    def disconnect(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def get_connection(self):
        return self.conn
