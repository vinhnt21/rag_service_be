from rag.generate_answer import get_answer

while True:
    print("Type 'exit' to exit.")
    question = input("Ask a question: ")
    if question == "exit":
        print("Goodbye!")
        break
    respone = get_answer(question)
    print(respone)
