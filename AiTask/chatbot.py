# rag_chatbot.py

from transformers import RagTokenizer, RagRetriever, RagSequenceForGeneration
import torch

class RAGChatbot:
    def __init__(self):
        # Initialize tokenizer, retriever, and model
        self.tokenizer = RagTokenizer.from_pretrained("facebook/rag-token-base")
        self.retriever = RagRetriever.from_pretrained(
            "facebook/rag-token-base",
            use_dummy_dataset=True,  # Use dummy dataset for simplicity
            trust_remote_code=True   # Trust remote code for loading dataset
        )
        self.model = RagSequenceForGeneration.from_pretrained("facebook/rag-token-base")

    def generate_response(self, query):
        # Tokenize the input query
        inputs = self.tokenizer(query, return_tensors="pt")

        # Retrieve documents relevant to the query
        retrieved_docs = self.retriever(inputs['input_ids'], return_tensors="pt")

        # Generate a response using the model and the retrieved documents
        outputs = self.model.generate(
            input_ids=inputs['input_ids'],
            context_input_ids=retrieved_docs['context_input_ids']
        )

        # Decode the generated response
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
