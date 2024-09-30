import os
import uuid

import streamlit as st

from localDB.localDB import LocalDB


class SearchEngine:
    def __init__(self, localDB = LocalDB()):
        self.localDB = localDB
        self.searchHis = []

    def search(self, query=""):
        if query == "":
            return self.localDB.getAll()
        result = self.localDB.searchTitle(query)
        return result




class SearchUI:
    def __init__(self, searchEngine = SearchEngine()):
        self.searchEngine = searchEngine
    def getCardUI(self, path):
        @st.dialog("Tóm tắt bài báo", width="large")
        def sumText(path):
            with open(path, 'r', encoding="utf-8") as f:
                paperSum = f.read()
            textBox = st.container(height=500)
            textBox.markdown(paperSum, unsafe_allow_html=True)
        sumText(path)
    def initUI(self):
        nCarPerRow = 3
        text_search = st.text_input("Search Summary of Paper", value="")
        result = self.searchEngine.search(text_search)

        if result:  # Kiểm tra nếu có kết quả
            nRow = len(result) // nCarPerRow + (len(result) % nCarPerRow > 0)  # Tính số hàng cần thiết

            for row in range(nRow):
                cols = st.columns(nCarPerRow)  # Tạo các cột cho mỗi hàng
                for col in range(nCarPerRow):
                    index = row * nCarPerRow + col
                    if index < len(result):  # Kiểm tra nếu còn kết quả để hiển thị
                        cardDetail = result[index]
                        with cols[col]:  # Đặt nội dung thẻ vào cột tương ứng
                            card = st.container(height=188, border=None)
                            titleBox = card.container(height=100, border=False)
                            titleBox.write(cardDetail[0])
                            card.button("Show Sum", on_click=self.getCardUI, args=(cardDetail[1],), key=uuid.uuid4() ,use_container_width=True)
        else:
            st.write("No results found.")

    def app(self):
        self.initUI()





app = SearchUI()
app.app()
