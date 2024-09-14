from flask import Flask, request, jsonify
from chatbot import Chatbot  # Ensure chatbot.py is in the same directory or adjust the import

app = Flask(__name__)
chatbot = Chatbot()

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400
    
    response = chatbot.generate_response(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(port=5000)
