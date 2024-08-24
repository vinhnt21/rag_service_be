import os
import pandas as pd
from bs4 import SoupStrainer
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag.rag_services import embeddings

# Thiết lập text_splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# Đường dẫn tới thư mục chứa các tệp CSV
folder_path = 'products_added'


# Định nghĩa hàm add_urls_to_vectorstore
def add_urls_to_vectorstore(urls: list, category_name) -> None:
    loader = WebBaseLoader(
        web_paths=urls,
        bs_kwargs=dict(
            parse_only=SoupStrainer(
                class_=("product-summary", "product-content__technical", "product-content__detail")
            )
        )
    )
    docs = loader.load()
    splits = text_splitter.split_documents(docs)
    print("Split documents::", len(splits))
    for split in splits:
        print(split)

    vectorstore = Chroma(persist_directory="./rag/vectorstore/" + category_name, embedding_function=embeddings)
    retriever = vectorstore.as_retriever()
    vectorstore.add_documents(splits)
    print("Added documents to vectorstore.")


# Kiểm tra xem thư mục có tồn tại hay không
if os.path.exists(folder_path):
    # Lặp qua tất cả các tệp trong thư mục
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        # Kiểm tra nếu là tệp CSV
        if os.path.isfile(file_path) and file_name.endswith('.csv'):
            print(f"Processing file: {file_name}")
            df = pd.read_csv(file_path)

            # Tạo một danh sách để lưu các chỉ mục đã cập nhật status
            updated_indices = []

            # Lặp qua các URL theo nhóm 20
            for start in range(0, len(df), 20):
                end = min(start + 20, len(df))
                urls = df['url'][start:end].tolist()

                try:
                    category_name = file_name.replace('.csv', '')
                    add_urls_to_vectorstore(urls, category_name)

                    # Cập nhật cột status thành 1 cho các dòng đã xử lý
                    df.loc[start:end - 1, 'status'] = 1
                    updated_indices.extend(range(start, end))

                except Exception as e:
                    print(f"Error processing URLs from {file_name} [{start}:{end}]: {str(e)}")

            # Ghi lại các thay đổi vào tệp CSV
            df.to_csv(file_path, index=False)
            print(f"Updated file: {file_name} with indices {updated_indices} set to status 1")
else:
    print(f'Thư mục "{folder_path}" không tồn tại.')
