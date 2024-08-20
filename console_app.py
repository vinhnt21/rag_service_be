from rag.generate_answer import ask

while True:
    print("Type 'exit' to exit.")
    question = input("Ask a question: ")
    if question == "exit":
        print("Goodbye!")
        break
    respone = ask(question)
    print("chat_history::", respone["chat_history"])
    print("answer::", respone["answer"])
    print("context::", respone["context"])
    print("`" * 80)
