from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag.rag_services import embeddings

vectorstore = Chroma(persist_directory="./rag/vectorstore", embedding_function=embeddings)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
retriever = vectorstore.as_retriever()


def add_urls_to_vectorstore(urls: list) -> None:
    loader = WebBaseLoader(urls)
    docs = loader.load()
    splits = text_splitter.split_documents(docs)
    vectorstore.add_documents(splits)
    print("Added documents to vectorstore.")




