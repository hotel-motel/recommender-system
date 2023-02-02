from databases import Database
from dotenv import dotenv_values


class DB:
    def __init__(self):
        db_config = dotenv_values('.env')
        self._host = db_config.get("DB_HOST")
        self._port = db_config.get("DB_PORT")
        self._db_name = db_config.get("DB_DATABASE")
        self._password = db_config.get("DB_PASSWORD")
        self._username = db_config.get("DB_USERNAME")
        self._connection = db_config.get("DB_CONNECTION")
        database_url = "{}://{}:{}@{}:{}/{}".format(self._connection, self._username, self._password, self._host, self._port, self._db_name)
        self._database = Database(database_url)

    @property
    def connection(self):
        return self._database