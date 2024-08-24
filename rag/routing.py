import ast
from typing import List

from langchain_core.prompts import ChatPromptTemplate

from rag.rag_services import llm


def get_list_vector_db_name() -> List[str]:
    try:
        import os
        directory_path = "vectorstore/"
        subfolders = [f.name for f in os.scandir(directory_path) if f.is_dir()]
        return subfolders
    except FileNotFoundError:
        #         print current directory
        print(os.getcwd())


vector_db_list = get_list_vector_db_name()


def validate_datasource(raw_datasource: List[str]) -> List[str]:
    res = []
    for source in raw_datasource:
        if source in vector_db_list:
            res.append(source)
        else:
            print(f"Error: {source} is not a valid datasource")
    return res


def convert_string_to_list(string: str) -> List[str]:
    try:
        return ast.literal_eval(string)
    except (ValueError, SyntaxError):
        print(f"Error: The string '{string}' is not a valid Python literal.")
        return []


def get_datasource(question: str) -> List[str]:
    print("=" * 50, "Getting datasource", sep="\n")
    system = """
    Bạn là một chuyên gia định tuyến câu hỏi của người dùng đến nguồn dữ liệu phù hợp nhất.
    Hãy chọn các nguồn dữ liệu phù hợp có thể chứa câu trả lời cho câu hỏi của người dùng trong các nguồn dữ liệu sau:
    {datasource}
    Câu trả lời cần tuân chủ chính xác format dưới và chỉ sử dụng các nguồn được cung cấp để có thể convert thành 
    list python:
    ["Nguồn 1", "Nguồn 2", "Nguồn 3"]
    ví dụ, câu hỏi là "Tôi muốn mua Kìm", bạn cần trả lời:
    ["Kìm cắt", "Kìm bấm lỗ"]
    Chú ý, chỉ được chọn nguồn dữ liệu từ datasource
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "{question}"),
        ]
    )
    print("Data source:", vector_db_list)
    # Define router
    router = prompt | llm
    res = router.invoke({
        "datasource": vector_db_list,
        "question": question
    })
    res = convert_string_to_list(res.content)
    res = validate_datasource(res)
    print("Num of datasource:", len(res))
    print("Datasource:", res)
    return res
