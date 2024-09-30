import os
from uuid import uuid4
import pandas as pd

class LocalDB:
    def __init__(self, localDBPath="localDB/localDB.csv", paperSumDir="localDB/paperSum"):
        self.localDBPath = localDBPath
        self.paperSumDir = paperSumDir
        self.localDB = None
        self.titleList = None
        self._initLocalDB()

    def _initLocalDB(self):
        if not os.path.exists(self.localDBPath):
            db = pd.DataFrame(columns=['id', 'title', 'path'])
            db.to_csv(self.localDBPath, index=False)
        if not os.path.exists(self.paperSumDir):
            os.mkdir(self.paperSumDir)
        db = pd.read_csv(self.localDBPath)
        self.localDB = db
        self.titleList = db.title.to_list()

    def addToDB(self, title):
        if title not in self.titleList:
            newPaperIndex = len(self.localDB)
            newPaperId = str(uuid4())
            newPaperNameFile = newPaperId + ".txt"
            newPaperPath = os.path.join(self.paperSumDir, newPaperNameFile)
            new_paper = {
                "id": newPaperId,
                "title": title,
                "path": newPaperPath
            }
            self.localDB.loc[newPaperIndex] = new_paper
            self._getAllTitles()
            self.localDB.to_csv(self.localDBPath, index=False)
            return newPaperPath

    def _getAllTitles(self):
        self.titleList = self.localDB.title.to_list()

    def getAll(self):
        if self.localDB.empty:
            return []
        return list(self.localDB[['title', 'path']].itertuples(index=False, name=None))

    def searchTitle(self, query):
        if not self.localDB.empty:
            # Tìm kiếm từ khóa trong danh sách tiêu đề
            results = self.localDB[self.localDB['title'].str.contains(query, case=False, na=False)]

            # Chuyển kết quả thành danh sách các tuple
            results_list = list(results[['title', 'path', 'id']].itertuples(index=False, name=None))

            return results_list
        return []
db = LocalDB()
