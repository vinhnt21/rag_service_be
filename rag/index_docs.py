from langchain.document_loaders.parsers.html import bs4
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag.rag_services import embeddings


text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)


def add_urls_to_vectorstore(urls: list, ) -> None:
    loader = WebBaseLoader(
        web_paths=urls,
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(
                class_=("product-summary", "product-content__technical", "product-content__detail")
            )
        )
    )
    docs = loader.load()
    splits = text_splitter.split_documents(docs)
    print("Split documents::", len(splits))
    for split in splits:
        print(split)
    print("Added documents to vectorstore.")
