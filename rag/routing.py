import ast
import logging
from typing import List

from langchain_core.prompts import ChatPromptTemplate

from rag.rag_services import llm


def get_list_vector_db_name() -> List[str]:
    directory_path = "./rag/vectorstore/"
    import os
    try:
        subfolders = []
        for name in os.listdir(directory_path):
            if os.path.isdir(os.path.join(directory_path, name)):
                subfolders.append(name)

        return subfolders
    except FileNotFoundError:
        logging.error(f"Directory not found: {directory_path}")
        logging.error(f"Current working directory: {os.getcwd()}")
        return []
    except Exception as e:
        logging.error(f"Error: {e}")
        return []


vector_db_list = get_list_vector_db_name()
print(f"Vector DB list: {vector_db_list}")


def validate_datasource(raw_datasource: List[str]) -> List[str]:
    res = []
    for source in raw_datasource:
        if source in vector_db_list:
            res.append(source)
        else:
            logging.error(f"Error: {source} is not a valid datasource")
    return res


def convert_string_to_list(string: str) -> List[str]:
    try:
        return ast.literal_eval(string)
    except (ValueError, SyntaxError):
        logging.error(f"Error: {string} is not a valid list")
        return []


def get_datasource(question: str) -> List[str]:
    print(f"Question: {question}\n----------------------")
    system = """
    Bạn là một chuyên gia định tuyến câu hỏi của người dùng đến nguồn dữ liệu phù hợp nhất.
    Hãy chọn các nguồn dữ liệu phù hợp có thể chứa câu trả lời cho câu hỏi của người dùng trong các nguồn dữ liệu sau:
    {datasource}
    Câu trả lời cần tuân chủ chính xác format dưới và chỉ sử dụng các nguồn được cung cấp để có thể convert thành 
    list python:
    ["Nguồn 1", "Nguồn 2", "Nguồn 3"]
    ví dụ, câu hỏi là "Tôi muốn mua Kìm", bạn cần trả lời:
    ["Kìm cắt", "Kìm bấm lỗ"]
    Chú ý, chỉ được chọn nguồn dữ liệu từ datasource, trả về đúng tên nguồn dữ liệu, không được thêm hoặc bớt bất kỳ ký tự nào
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "{question}"),
        ]
    )
    print(f"Data source: {vector_db_list}")
    # Define router
    router = prompt | llm
    res = router.invoke({
        "datasource": vector_db_list,
        "question": question
    })
    res = convert_string_to_list(res.content)
    res = validate_datasource(res)
    print(f"Number of datasource: {len(res)}")
    print(f"Datasource: {res}")
    return res
