from typing import List

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

from rag.rag_services import embeddings, llm
from rag.routing import get_datasource

system_prompt = (
    '''
    Bạn là chuyên viên tư vấn bán hàng cho SuperMRO
    Bạn có nhiệm vụ trả lời câu hỏi của khách hàng về sản phẩm và dịch vụ của công ty dựa trên ngữ cảnh và lịch sử 
    trò chuyện được cung cấp bên dưới đây
    
    Ngữ cảnh:
    {context}
    
    
    Yêu cầu về câu trả lời:
    - Trả lời theo định dạng markdown
    - Nếu câu hỏi về so sánh các sản phẩm, hãy trình bày ở dạng bảng
    - Nếu câu hỏi chung chung về 1 loại sản phẩm, hãy giới thiệu và đặt câu hỏi gợi mở để khách hàng có thể hiểu rõ hơn về sản phẩm
    - Nếu bạn không biết câu trả lời, hãy nói rằng bạn không biết
    - Chỉ sử dụng tiếng Việt
    - Giới hạn số từ tối đa: 800 từ 
    
    
    Lịch sử trò chuyện:
    {chat_history}
    '''
)


def get_relevant_document(question: str, data_sources: List[str]) -> list[Document]:
    res = []
    for data_source in data_sources:
        vector_db = Chroma(persist_directory=f'vectorstore/{data_source}', embedding_function=embeddings)
        context = vector_db.similarity_search(question)
        print("Number of context:", len(context))
        # log context in to txt file
        with open(f"rag_context_{data_source}.txt", "w", encoding="utf-8") as f:
            for c in context:
                s = str(c)
                f.write(s + "\n")
                f.write("=" * 50 + "\n")
        res.extend(context)
    return res


chat_history = []


def get_answer(question: str) -> str:
    data_sources = get_datasource(question)
    relevant_documents = get_relevant_document(question, data_sources)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    chain = prompt | llm
    res = chain.invoke({
        "context": relevant_documents,
        "input": question,
        "chat_history": chat_history
    })

    chat_history.append([
        ("human", question),
        ("system", res.content)
    ])
    return res.content
