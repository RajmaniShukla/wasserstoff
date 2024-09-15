# app.py
from flask import Flask, request, jsonify
from chatbot import Chatbot

# Initialize Flask application
app = Flask(__name__)

# Initialize the chatbot instance
chatbot = Chatbot()

@app.route('/suggest', methods=['POST'])
def suggest():
    # Parse the incoming JSON request
    data = request.get_json()
    # Extract the 'query' field from the JSON data
    query = data.get('query', '')
    
    # Check if 'query' is provided; return an error if not
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    # Generate a response from the chatbot using the provided query
    response = chatbot.generate_response(query)
    # Return the response in JSON format
    return jsonify({'suggestion': response})

# Run the Flask application in debug mode if this script is executed
if __name__ == '__main__':
    app.run(debug=True)
