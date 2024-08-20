from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from rag.rag_services import llm
from rag.index_docs import retriever
from langchain_core.messages import AIMessage, HumanMessage

system_prompt = (
    "Bạn là một trợ lý cho các nhiệm vụ trả lời câu hỏi. "
    "Sử dụng các phần ngữ cảnh được lấy ra dưới đây để trả lời câu hỏi. "
    "Nếu bạn không biết câu trả lời, hãy nói rằng bạn không biết. "
    "Trả lời ngắn gọn trong ba câu và giữ cho câu trả lời súc tích."
    "\n\n"
    "{context}"
)

contextualize_q_system_prompt = (
    "Dựa trên lịch sử trò chuyện và câu hỏi mới nhất của người dùng "
    "có thể tham chiếu đến ngữ cảnh trong lịch sử trò chuyện, "
    "hãy tạo ra một câu hỏi độc lập có thể hiểu được mà không cần đến lịch sử trò chuyện. "
    "KHÔNG trả lời câu hỏi, chỉ cần điều chỉnh lại nếu cần thiết, nếu không thì giữ nguyên."
)

contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)

qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

chat_history = []


def ask(question: str) -> str:
    global chat_history
    response = rag_chain.invoke({"input": question, "chat_history": chat_history})
    chat_history.extend(
        [
            HumanMessage(content=question),
            AIMessage(content=response["answer"]),
        ]
    )
    return response
