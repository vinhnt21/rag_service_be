from langchain_cohere import CohereEmbeddings, ChatCohere
from dotenv import load_dotenv

load_dotenv()
embeddings = CohereEmbeddings(
    model="embed-multilingual-light-v3.0"
)

llm = ChatCohere(
    model="command-r-plus",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)