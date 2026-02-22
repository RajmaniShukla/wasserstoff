# Wasserstoff - AI Chatbot 🤖

A modern, lightweight chatbot powered by GPT-2 with both a Flask API backend and a WordPress plugin frontend.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- **GPT-2 Powered**: Uses Hugging Face Transformers for intelligent responses
- **REST API**: Clean Flask API with proper error handling
- **WordPress Integration**: Beautiful floating chatbot widget
- **GPU Support**: Automatic GPU detection for faster inference
- **Configurable**: Adjustable temperature, max length, and sampling parameters
- **Modern UI**: Sleek, responsive chat interface

## 📁 Project Structure

```
wasserstoff/
├── AiTask/
│   ├── app.py          # Flask API server
│   └── chatbot.py      # GPT-2 chatbot class
├── wp_plugin/
│   ├── wp-chatbot.php  # WordPress plugin main file
│   ├── hooks.php       # WordPress hooks
│   └── js/
│       └── chatbot.js  # Frontend chat widget
├── requirements.txt    # Python dependencies
└── README.md
```

## 🚀 Quick Start

### Backend Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/RajmaniShukla/wasserstoff.git
   cd wasserstoff
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server:**
   ```bash
   cd AiTask
   python app.py
   ```

   The API will be available at `http://127.0.0.1:5000`

### WordPress Setup

1. Copy the `wp_plugin` folder to your WordPress `wp-content/plugins/` directory
2. Activate the plugin from WordPress admin
3. Update the API URL in `js/chatbot.js` if needed

## 📡 API Endpoints

### Health Check
```http
GET /
```

**Response:**
```json
{
  "status": "healthy",
  "service": "GPT-2 Chatbot API",
  "version": "1.0.0"
}
```

### Generate Response
```http
POST /suggest
Content-Type: application/json

{
  "query": "What is artificial intelligence?",
  "temperature": 0.7,
  "max_length": 100
}
```

**Response:**
```json
{
  "suggestion": "Artificial intelligence is..."
}
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | string | required | The input prompt |
| `temperature` | float | 0.7 | Controls randomness (0-2) |
| `max_length` | int | 100 | Maximum response length (1-500) |

## 🎨 Chat Widget Features

- 💬 Floating chat button with smooth animations
- 📱 Fully responsive design (mobile-friendly)
- ⌨️ Typing indicators while generating response
- 🎯 XSS protection for user messages
- ✨ Modern UI with gradient accents

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 5000 | Server port |
| `DEBUG` | true | Enable debug mode |

### Chatbot Parameters

Edit `AiTask/chatbot.py` to customize:

```python
MAX_INPUT_LENGTH = 512   # Max input tokens
MAX_OUTPUT_LENGTH = 100  # Max output tokens
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [Flask](https://flask.palletsprojects.com/)
- [GPT-2 by OpenAI](https://openai.com/blog/gpt-2-1-5b-release/)

---

Made with ❤️ by [Rajmani Shukla](https://github.com/RajmaniShukla)
