# chatbot.py
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

class Chatbot:
    def __init__(self, model_name='gpt2'):
        # Load pre-trained GPT-2 tokenizer and model
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        # Define maximum input and output lengths for the model
        self.MAX_INPUT_LENGTH = 512
        self.MAX_OUTPUT_LENGTH = 100

    def generate_response(self, prompt):
        # Encode the input prompt into token ids, truncate if necessary
        inputs = self.tokenizer.encode(prompt, return_tensors='pt', max_length=self.MAX_INPUT_LENGTH, truncation=True)
        # Generate a response from the model
        outputs = self.model.generate(
            inputs,
            # Set the maximum length of the output sequence
            max_length=self.MAX_INPUT_LENGTH + self.MAX_OUTPUT_LENGTH,
            # Generate only one sequence of text
            num_return_sequences=1,
            # Stop generating when an end-of-sequence token is encountered
            early_stopping=True,
            # Adjust the randomness of the generated text
            temperature=0.7,  
            # Limit the number of highest probability vocabulary tokens to keep for each generation step
            top_k=50,         
            # Use nucleus sampling to limit the cumulative probability threshold
            top_p=0.95,       
            # Prevent the generation of repeating n-grams
            no_repeat_ngram_size=2  
        )
        # Decode the generated tokens to a readable string
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(response)
        return response
