from sqlalchemy import create_engine,text
import pymssql

class Database:
    def __init__(self, connection_string = None):
        if(connection_string is None):
            connection_string = ''
        self.engine = create_engine(connection_string)

    def execute_first(self, sql, params=None):
        with self.engine.connect() as conn:
            result = conn.execute(text(sql), params)
            return result.fetchone()

    def execute_query(self, sql, params=None):
        with self.engine.connect() as conn:
            result = conn.execute(text(sql), params)
            return result

    def execute_insert(self, sql, params=None):
        with self.engine.connect() as conn:
            result = conn.execute(text(sql), params)
            conn.commit()
            return result.rowcount

    def execute_update(self, sql, params=None):
        with self.engine.connect() as conn:
            result = conn.execute(text(sql), params)
            return result.rowcount

    def execute_delete(self, sql, params=None):
        with self.engine.connect() as conn:
            result = conn.execute(text(sql), params)
            return result.rowcount
