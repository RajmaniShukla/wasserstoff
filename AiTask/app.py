"""
Flask API for the GPT-2 Chatbot.
"""
import os
import logging
from typing import Tuple, Dict, Any

from flask import Flask, request, jsonify, Response
from flask_cors import CORS

from chatbot import Chatbot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize chatbot (singleton)
chatbot: Chatbot = None


def get_chatbot() -> Chatbot:
    """Get or create the chatbot instance (lazy loading)."""
    global chatbot
    if chatbot is None:
        logger.info("Initializing chatbot...")
        chatbot = Chatbot()
    return chatbot


@app.route('/', methods=['GET'])
def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'GPT-2 Chatbot API',
        'version': '1.0.0'
    })


@app.route('/suggest', methods=['POST'])
def suggest() -> Tuple[Response, int]:
    """
    Generate a suggestion/response based on the query.
    
    Request JSON:
        {
            "query": "Your question here",
            "temperature": 0.7,  // optional
            "max_length": 100    // optional
        }
    
    Response JSON:
        {
            "suggestion": "Generated response"
        }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'No query provided'}), 400
        
        # Optional parameters
        temperature = data.get('temperature', 0.7)
        max_length = data.get('max_length', 100)
        
        # Validate parameters
        if not isinstance(temperature, (int, float)) or not 0 < temperature <= 2:
            return jsonify({'error': 'Temperature must be between 0 and 2'}), 400
        
        if not isinstance(max_length, int) or max_length < 1 or max_length > 500:
            return jsonify({'error': 'max_length must be between 1 and 500'}), 400
        
        # Generate response
        bot = get_chatbot()
        response = bot.generate_response(
            query,
            temperature=float(temperature),
            max_length=int(max_length)
        )
        
        logger.info(f"Query: {query[:50]}... -> Response generated")
        
        return jsonify({'suggestion': response}), 200
        
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@app.errorhandler(404)
def not_found(error) -> Tuple[Response, int]:
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error) -> Tuple[Response, int]:
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'true').lower() == 'true'
    
    logger.info(f"Starting server on port {port} (debug={debug})")
    app.run(host='0.0.0.0', port=port, debug=debug)
