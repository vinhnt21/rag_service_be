from encode_context import *

context = '''
Mary and Peter transferred 15,000 EUR from HSBC bank in London to the account of ABC Company in Switzerland on July 15, 2023.
'''
question = '''
How many EUR did Mary and Peter transfer ?
'''
print("Raw context:", context)
print("Raw question:", question)
# Encode the context and question
print("Encoding context and question...")
word_list_str = detect_words(context, question)
# convert the string to a list of tuples
import ast

words_list = ast.literal_eval(word_list_str)
print("Words list:", words_list)
context_abstract, question_abstract = make_context_abstract(context, question, words_list)
print("Encoded context:", context_abstract)
print("Encoded question:", question_abstract)
abstract_answer = send_to_cloud_model(context_abstract, question_abstract)
print("Abstract answer:", abstract_answer)
decoded_answer = decode_answer(abstract_answer, words_list)
print("Decoded answer:", decoded_answer)
