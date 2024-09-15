# chatbot.py
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

class Chatbot:
    def __init__(self, model_name='gpt2'):
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        self.MAX_INPUT_LENGTH = 512
        self.MAX_OUTPUT_LENGTH = 100

    def generate_response(self, prompt):
        inputs = self.tokenizer.encode(prompt, return_tensors='pt', max_length=self.MAX_INPUT_LENGTH, truncation=True)
        outputs = self.model.generate(
            inputs,
            max_length=self.MAX_INPUT_LENGTH + self.MAX_OUTPUT_LENGTH,
            num_return_sequences=1,
            early_stopping=True,
            temperature=0.7,  # Adjust temperature for randomness
            top_k=50,         # Control the diversity of the generated text
            top_p=0.95,       # Nucleus sampling: cumulative probability threshold
            no_repeat_ngram_size=2  # Prevent repetition of n-grams
        )
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
