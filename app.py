from flask import Flask, request
from flask_cors import CORS

from rag.generate_answer import ask

app = Flask(__name__)

CORS(app)


@app.before_request
def handle_options_requests():
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        headers = response.headers

        headers['Access-Control-Allow-Origin'] = '*'
        headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'

        return response


@app.route('/ask', methods=['POST'])
def route_ask():
    """
    get question form request body and return answer
    :return:
    """
    question = request.json.get('question')
    try:
        response = ask(question)
    except Exception as e:
        return {
            "message": f"Error occurred: {e}"
        }
    return {
        "message": response["answer"]
    }


if __name__ == '__main__':
    app.run()
