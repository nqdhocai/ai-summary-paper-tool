import os
import sqlite3
from uuid import uuid4


class LocalDB:
    def __init__(self, data_dir="localDB", db_name: str = "localDB\local.db",
                 title_table_name: str = "paper_summarized",
                 store_path: str = "localDB\paper_summarized"):
        self.data_dir = data_dir
        self.store_path = store_path
        self._init_data_dir()

        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.title_table_name = title_table_name

        self._init_table()

    def _init_data_dir(self):
        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)
        if not os.path.exists(self.store_path):
            os.mkdir(self.store_path)

    def _init_table(self):
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.title_table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                path TEXT NOT NULL
            )
        ''')

        self.conn.commit()

    def _is_paper_exist(self, title: str) -> bool:
        title = title.upper()
        self.cursor.execute("SELECT * FROM paper_summarized WHERE title = ?", (title,))
        result = self.cursor.fetchone()
        if result is None:
            return False
        return True

    def insert_paper(self, title: str):
        title = title.upper()
        if not self._is_paper_exist(title):
            paper_file_path = str(uuid4()) + ".txt"
            paper_file_path = os.path.join(self.store_path, paper_file_path)

            self.cursor.execute(f"""
            INSERT INTO {self.title_table_name} (title, path) 
            VALUES (?, ?)
            """, (title, paper_file_path,))
            self.conn.commit()
            print("inserted new paper")

            self.conn.commit()
            return paper_file_path
        else:
            print("paper is existed")
            return None

    def get_paper_path(self, title: str = ""):
        title = title.upper()
        if not self._is_paper_exist(title):
            return None
        self.cursor.execute(f"SELECT * FROM {self.title_table_name} WHERE title = ?", (title,))
        result = self.cursor.fetchone()
        path = result[-1]

        return path

    def get_all_papers(self) -> list:
        self.cursor.execute(f"SELECT * FROM {self.title_table_name}")
        result = self.cursor.fetchall()
        return result # [(id, title, path)]

    def search_paper(self, query=""):
        self.cursor.execute(f"""
            SELECT * FROM {self.title_table_name}
            WHERE title LIKE ?
        """, (f"%{query.upper()}%",))
        result = self.cursor.fetchall()
        return result # [(id, title, path)]
