import os
import sqlite3

import pandas as pd
import pandas.io.sql


class SqlConnectionManager:
    def __init__(self, db_file: str):
        self.create_dirs(db_file)
        self.connection = sqlite3.connect(f'sql/{db_file}', isolation_level=None,
                                          detect_types=sqlite3.PARSE_COLNAMES)
        self.create_excel_files(db_file)

    def create_dirs(self, db_file: str):
        try:
            os.makedirs(os.path.join('excel', db_file.split('.')[0]))
        except (Exception, FileExistsError):
            ...

    def create_excel_files(self, file: str):
        tables = self.get_tables_list()
        for table in tables:
            pd.read_sql_query(f'SELECT * FROM {table};', self.connection). \
                to_excel(f'excel/{file.split(".")[0]}/{table}.xlsx', index=True)

    def get_tables_list(self) -> list[str]:
        return ';'.join(map(str, pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';",
                                                   self.connection).values.tolist())). \
            replace('[\'', '').replace('\']', '').split(';')
