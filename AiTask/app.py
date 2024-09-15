# app.py
from flask import Flask, request, jsonify
from chatbot import Chatbot

app = Flask(__name__)

# Initialize the chatbot
chatbot = Chatbot()

@app.route('/suggest', methods=['POST'])
def suggest():
    data = request.get_json()
    query = data.get('query', '')
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    response = chatbot.generate_response(query)
    return jsonify({'suggestion': response})

if __name__ == '__main__':
    app.run(debug=True)
