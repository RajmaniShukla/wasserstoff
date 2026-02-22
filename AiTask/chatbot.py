"""
Chatbot module using GPT-2 for text generation.
"""
from typing import Optional
import logging

import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Chatbot:
    """A chatbot class that uses GPT-2 for generating responses."""
    
    # Default configuration
    DEFAULT_MODEL = 'gpt2'
    MAX_INPUT_LENGTH = 512
    MAX_OUTPUT_LENGTH = 100
    
    def __init__(self, model_name: str = DEFAULT_MODEL) -> None:
        """
        Initialize the chatbot with a pre-trained GPT-2 model.
        
        Args:
            model_name: The name of the pre-trained model to use.
        """
        logger.info(f"Loading model: {model_name}")
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        
        # Set padding token
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Use GPU if available
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
        logger.info(f"Model loaded successfully on {self.device}")

    def generate_response(
        self,
        prompt: str,
        temperature: float = 0.7,
        top_k: int = 50,
        top_p: float = 0.95,
        max_length: Optional[int] = None
    ) -> str:
        """
        Generate a response based on the input prompt.
        
        Args:
            prompt: The input text to generate a response for.
            temperature: Controls randomness (higher = more random).
            top_k: Limits vocabulary to top k tokens.
            top_p: Nucleus sampling threshold.
            max_length: Maximum output length (uses default if None).
            
        Returns:
            The generated text response.
            
        Raises:
            ValueError: If prompt is empty.
        """
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")
        
        max_output = max_length or self.MAX_OUTPUT_LENGTH
        
        # Encode input
        inputs = self.tokenizer.encode(
            prompt,
            return_tensors='pt',
            max_length=self.MAX_INPUT_LENGTH,
            truncation=True
        ).to(self.device)
        
        # Generate response
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_length=self.MAX_INPUT_LENGTH + max_output,
                num_return_sequences=1,
                early_stopping=True,
                temperature=temperature,
                top_k=top_k,
                top_p=top_p,
                no_repeat_ngram_size=2,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        # Decode and return
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        logger.debug(f"Generated response: {response[:100]}...")
        
        return response


# For testing
if __name__ == '__main__':
    bot = Chatbot()
    test_prompt = "What is artificial intelligence?"
    print(f"Prompt: {test_prompt}")
    print(f"Response: {bot.generate_response(test_prompt)}")
