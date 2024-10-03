import os

import streamlit as st

from aicore import summarize_text
from localDB.localDB import LocalDB
from rag import VectorDB

HIS_DIR = "localDB\paperSum"
LocalDB = LocalDB()
VectorDB = VectorDB()


# Hàm trích xuất văn bản từ file PDF
def save_uploaded_file(uploaded_file):
    # Đường dẫn thư mục lưu file
    save_dir = "../asset"

    # Tạo thư mục nếu chưa có
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Đường dẫn đầy đủ của file
    file_path = os.path.join(save_dir, uploaded_file.name)

    # Lưu file vào thư mục
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


if "curSum" not in st.session_state:
    st.session_state.curSum = ""
# Giao diện Streamlit
st.title("Tóm tắt Paper PDF")

# Tạo khung upload file PDF
uploaded_file = st.file_uploader("Tải lên file PDF", type="pdf")

# Khi có file được tải lên
if uploaded_file is not None:
    # Nút bấm để tóm tắt
    if st.button("Tóm tắt"):
        # Hiển thị loading
        with st.spinner("Đang tóm tắt..."):
            path = save_uploaded_file(uploaded_file)
            # Tóm tắt văn bản
            sum_text = summarize_text(path)
            title = sum_text.split("\n")[0]
            for i in ["#", "Tóm tắt bài báo:", "Tóm tắt bài báo", "Tóm tắt", ":"]:
                if i in title:
                    title = title.replace(i, "")
            paperSumPath = LocalDB.insert_paper(title)
            if paperSumPath is not None:
                with open(paperSumPath, "w", encoding="utf-8") as f:
                    f.write(sum_text)
                VectorDB.add_doc_by_path(paperSumPath)
            os.remove(path)
        st.markdown("### Tóm tắt:")
        sum_box = st.container(height=800)
        # Hiển thị kết quả dưới dạng markdown
        sum_box.markdown(sum_text)
