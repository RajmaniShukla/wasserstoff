from flask import Flask, request, jsonify
from transformers import RagTokenizer, RagRetriever, RagSequenceForGeneration

# Initialize the RAG model and tokenizer
tokenizer = RagTokenizer.from_pretrained("facebook/rag-sequence-nq")
retriever = RagRetriever.from_pretrained("facebook/rag-sequence-nq",use_dummy_dataset=True)
model = RagSequenceForGeneration.from_pretrained("facebook/rag-sequence-nq")

# Initialize Flask
app = Flask(__name__)

def generate_suggestions(query):
    inputs = tokenizer(query, return_tensors="pt")
    generated = model.generate(**inputs)
    suggestion = tokenizer.batch_decode(generated, skip_special_tokens=True)
    return suggestion[0]

@app.route('/suggest', methods=['POST'])
def suggest():
    data = request.get_json()
    query = data.get('query', '')
    
    if not query:
        return jsonify({"error": "No query provided"}), 400

    suggestion = generate_suggestions(query)
    return jsonify({"suggestion": suggestion})

if __name__ == '__main__':
    app.run(debug=True)
