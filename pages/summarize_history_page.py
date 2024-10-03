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
            return self.localDB.get_all_papers()
        result = self.localDB.search_paper(query)
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

        text_search = st.text_input("Search Summary of Paper", value="")
        results = self.searchEngine.search(text_search)

        if results:  # Kiểm tra nếu có kết quả
            num_results = len(results)
            st.markdown(f"***Number of search results: {num_results}***")
            for item in results:
                col1, col2 = st.columns([30, 5], vertical_alignment="center")
                col1.markdown(f" *{item[1]}")
                col2.button("Details", on_click=self.getCardUI, key=item[-1],args=(item[-1],))

                st.markdown("---")

        else:
            st.write("No results found.")

    def app(self):
        self.initUI()


app = SearchUI()
app.app()
