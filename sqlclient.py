from contextlib import contextmanager

from sqlalchemy import create_engine

"""
Usage example:
client = SqlClient(Config())
with client.get_conn() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())
"""
class SqlClient:
    def __init__(self, config):
        db_connect_string = f"mysql+pymysql://{config.user}:{config.password}@{config.host}:{config.port}"
        ssl_args = {
            'ssl':
                {'ca': config.ca_path}
        }

        self.engine = create_engine(db_connect_string, connect_args=ssl_args)

    @contextmanager
    def get_conn(self):
        with self.engine.connect() as connection:
            yield connection

