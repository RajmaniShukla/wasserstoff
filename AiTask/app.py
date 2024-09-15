from flask import Flask, request, jsonify
from chatbot import generate_response

app = Flask(__name__)

@app.route('/suggest', methods=['POST'])
def suggest():
    data = request.json
    user_query = data.get('query', '')

    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    # Generate a suggestion based on the user's query
    suggestion = generate_response(user_query)
    
    return jsonify({"suggestion": suggestion})

if __name__ == '__main__':
    app.run(debug=True)
