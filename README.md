# 🤖 Zed-BOT – AI Chatbot with Knowledge Base + GPT-2

This is a hybrid chatbot built using Streamlit and Hugging Face Transformers. It responds using either a predefined intent-based knowledge base or generates responses using GPT-2 when no match is found.

---

## ✅ Features

- Friendly chatbot interface
- Two modes of response:
  - Intent-based replies (from `intents.json`)
  - GPT-2 generated responses
- Maintains chat history with timestamps
- Button to clear chat history

---

## 🧠 Tech Stack

- Python
- Streamlit
- Hugging Face Transformers (GPT-2)
- JSON (for intent patterns and responses)

---

## ▶️ How to Run

1. Install dependencies:
   pip install streamlit transformers

Make sure you have an intents.json file in the same directory. Sample format:
{
  "intents": [
    {
      "tag": "greeting",
      "patterns": ["hi", "hello", "hey"],
      "responses": ["Hello!", "Hi there!"]
    },
    {
      "tag": "joke",
      "patterns": ["tell me a joke", "make me laugh"],
      "responses": ["Why did the chicken cross the road? To get to the other side!"]
    }
  ]
}

Run the app:
streamlit run ChatBot_Project.py

🔧 Project Structure
├── ChatBot_Project.py       # Main Streamlit chatbot code
├── intents.json             # Intent-based knowledge base
├── README.md                # Project instructions

📌 Notes
Make sure you’re connected to the internet to load GPT-2 from Hugging Face.
Custom responses can be added in the intents.json.
