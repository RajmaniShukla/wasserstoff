from transformers import GPT2LMHeadModel, GPT2Tokenizer

class Chatbot:
    def __init__(self):
        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        self.model = GPT2LMHeadModel.from_pretrained('gpt2')

    def generate_response(self, prompt):
        inputs = self.tokenizer.encode(prompt, return_tensors='pt')
        outputs = self.model.generate(inputs, max_length=150, num_return_sequences=1)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response

if __name__ == "__main__":
    chatbot = Chatbot()
    user_input = "Hello, how can I help you today?"
    print(chatbot.generate_response(user_input))