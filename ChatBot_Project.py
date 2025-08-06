import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
from datetime import datetime
import json
import random  

class ChatBot:
    def __init__(self, model_name="gpt2", knowledge_base_file="intents.json"):
        self.model_name = model_name
        self.chatbot_model, self.tokenizer = self.load_model()
        self.knowledge_base = self.load_knowledge_base(knowledge_base_file)

    def load_model(self):
        """Load the GPT-2 model and tokenizer with error handling."""
        try:
            tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            model = AutoModelForCausalLM.from_pretrained(self.model_name)
            return model, tokenizer
        except Exception as e:
            print(f"Error loading model: {e}")
            st.error("Error loading model. Please check the model name or internet connection.")
            return None, None

    def load_knowledge_base(self, file_path):
        """Load predefined knowledge base from an intents JSON file with error handling."""
        knowledge_base = {}
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                knowledge_base = json.load(file)
        except FileNotFoundError:
            st.error(f"Knowledge base file '{file_path}' not found. Using empty knowledge base.")
        except Exception as e:
            st.error(f"Error loading knowledge base: {e}")
        return knowledge_base

    def find_knowledge_base_response(self, user_input):
        """Search for user input in the knowledge base."""
        for intent in self.knowledge_base['intents']:
            for pattern in intent['patterns']:
                if pattern.lower() in user_input.lower():
                    if intent['tag'] == "joke":
                        return random.choice(intent['responses'])
                    else:
                        return random.choice(intent['responses'])
        return None

    def generate_gpt2_response(self, user_input):
        """Generate response using GPT-2."""
        inputs = self.tokenizer.encode(user_input + self.tokenizer.eos_token, return_tensors="pt")
        outputs = self.chatbot_model.generate(inputs, max_length=100, pad_token_id=self.tokenizer.eos_token_id, no_repeat_ngram_size=2)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response

    def generate_response(self, user_input):
        """Generate response based on knowledge base or GPT-2."""
        if not user_input.strip():
            return "Please type something for me to respond to!"

        knowledge_response = self.find_knowledge_base_response(user_input)
        if knowledge_response:
            return knowledge_response

        return self.generate_gpt2_response(user_input)

chatbot = ChatBot()

st.title("Zed-BOT")
st.write("Ask me anything!")

if 'history' not in st.session_state:
    st.session_state.history = []
if 'last_input' not in st.session_state:
    st.session_state.last_input = ""

def get_response(user_input):
    """Generate chatbot response and store it in the session history."""
    timestamp = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    chatbot_response = chatbot.generate_response(user_input)

    st.session_state.history.append((timestamp, user_input, chatbot_response))
    return chatbot_response

user_input = st.text_input("Your message:")

if user_input and user_input != st.session_state.last_input:
    chatbot_response = get_response(user_input)
    st.session_state.last_input = user_input
    st.write(f"### Current Response")
    st.write(f"**Bot:** {chatbot_response}")

if st.button("Show Chat History"):
    st.write("### Chat History")
    for timestamp, user_msg, bot_msg in reversed(st.session_state.history):
        st.write(f"**{timestamp} - User:** {user_msg}")
        st.write(f"**{timestamp} - Bot:** {bot_msg}")

if st.button("Clear Chat History"):
    st.session_state.history = []
    st.session_state.last_input = ""  
    st.write("Chat history cleared!")
