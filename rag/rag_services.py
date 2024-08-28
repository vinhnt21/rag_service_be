from langchain_cohere import CohereEmbeddings, ChatCohere
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv()
embeddings = CohereEmbeddings(
    model="embed-multilingual-light-v3.0"
)

llm = ChatCohere(
    model="command-r-plus",
    temperature=0,
    max_tokens=None,
    timeout=None,
)


#
# llm = ChatOpenAI(
#     model="gpt-4o-mini",  # Đảm bảo không có dấu cách sau model
#     temperature=0,
#     max_tokens=None,
#     timeout=None,
#     max_retries=2,
#     # api_key="...",  # Nếu muốn cung cấp API key trực tiếp
#     # base_url="...",
#     # organization="...",
# )
