import google.generativeai as genai
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity  # Thêm import cho cosine_similarity
import re
import chromadb
import os

# Cấu hình API
def get_embeddings(sens):
    embeddings = genai.embed_content(
        model="models/text-embedding-004",
        content=sens,
        task_type="retrieval_document",
        title="Embedding of doc string"
    )
    return np.array(embeddings['embedding'])

class ChunkingRag:
    def __init__(self, api_key="GOOGLE_API_KEY"):
        genai.configure(api_key=api_key)

    def preprocess_text(self, text):
        # Bước 1: Xóa các ký tự không cần thiết
        text = re.sub(r'\*\*|\*|#', '', text)  # Xóa các dấu hiệu markdown
        text = text.strip()  # Xóa khoảng trắng ở đầu và cuối
        text = text.replace("\n", "")
        return text
    def get_embeddings(self, sens):
        embeddings = genai.embed_content(
            model="models/text-embedding-004",
            content=sens,
            task_type="retrieval_document",
            title="Embedding of doc string"
        )
        return np.array(embeddings['embedding'])

    def semantic_chunking(self, text, threshold=0.8):
        text = self.preprocess_text(text)

        # Phân đoạn văn bản thành các câu
        sentences = text.split('. ')

        # Tạo nhúng cho từng câu
        embeddings = self.get_embeddings(sentences)

        # Tính toán độ tương đồng cosine giữa các câu
        cosine_similarities = cosine_similarity(embeddings)  # Sử dụng cosine_similarity từ sklearn

        # Danh sách để lưu các chunk
        chunks = []
        current_chunk = []

        for i in range(len(sentences)):
            current_chunk.append(sentences[i])

            # Kiểm tra độ tương đồng với câu tiếp theo
            if i < len(sentences) - 1 and cosine_similarities[i][i + 1] < threshold:
                # Nếu độ tương đồng thấp hơn ngưỡng, lưu chunk hiện tại
                chunks.append(' '.join(current_chunk))
                current_chunk = []

        # Thêm chunk cuối cùng nếu có
        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks

class VectorDB:
    def __init__(self, localDB="localDB", collection_name="rag", chunking_model=ChunkingRag(), doc_dir="localDB\paper_summarized"):
        self.client = chromadb.PersistentClient(localDB)
        self.collection_name = collection_name
        self.chunking_model=chunking_model
        self.doc_dir = doc_dir
        self._init_db()

    def _init_db(self):
        try:
            self.collection = self.client.get_collection(self.collection_name)
        except:
            self.client.create_collection(self.collection_name)
            self.collection = self.client.get_collection(self.collection_name)
            doc_paths = os.listdir(self.doc_dir)
            chunks = []
            for doc_path in doc_paths:
                id = doc_path.replace(".txt", "")
                with open(os.path.join(self.doc_dir, doc_path), 'r', encoding="utf-8") as f:
                    doc_chunks = self.chunking_model.semantic_chunking(f.read())
                    for i, chunk in enumerate(doc_chunks):
                        chunks.append((str(id) + str(i), chunk))
            self.add_docs(chunks)

    def add_docs(self, docs):
        self.collection.add(
            documents=[doc[1] for doc in docs],
            ids=[doc[0] for doc in docs]
        )
    def add_doc_by_path(self, path):
        chunks = []
        id = path.split("\\")[-1].replace(".txt", "")
        with open(path, 'r', encoding="utf-8") as f:
            doc_chunks = self.chunking_model.semantic_chunking(f.read())
            for i, chunk in enumerate(doc_chunks):
                chunks.append((str(id) + str(i), chunk))
        self.add_docs(chunks)
    def get_docs(self, query, limit=10):
        results = self.collection.query(
            query_texts=[query],  # Chroma will embed this for you
            n_results=limit  # how many results to return
        )
        return results['documents']
