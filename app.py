
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
import os

# Set page config FIRST - before any other Streamlit commands
st.set_page_config(page_title="Ritvik Varghese - AI Chat", layout="wide")

load_dotenv(override=True)
openai = OpenAI()

# Load data
@st.cache_data
def load_data():
    reader = PdfReader("me/linkedin.pdf")
    linkedin = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            linkedin += text

    with open("me/summary.txt", "r", encoding="utf-8") as f:
        summary = f.read()

    return linkedin, summary

linkedin, summary = load_data()
name = "Ritvik Varghese"

system_prompt = f"""You are acting as {name}. You are answering questions on {name}'s website, 
particularly questions related to {name}'s career, background, skills and experience. 
Your responsibility is to represent {name} for interactions on the website as faithfully as possible. 
You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. 
Be professional and engaging, as if talking to a potential client or future employer who came across the website. 
If you don't know the answer, say so.

## Summary:
{summary}

## LinkedIn Profile:
{linkedin}

With this context, please chat with the user, always staying in character as {name}."""

def chat(message, history):
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model="gpt-4o-mini", messages=messages)
    return response.choices[0].message.content

# Streamlit UI with Enhanced Chat Styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 0.5rem;
    }
    .main-header h1 {
        color: #fff;
        font-size: 2rem;
        margin-bottom: 0.3rem;
        font-family: 'Manrope', sans-serif;
    }
    .main-header p {
        color: #ccc;
        font-size: 1rem;
        margin: 0 0 0.5rem 0;
        font-family: 'Manrope', sans-serif;
    }
    .contact-links {
        text-align: center;
        padding: 0.5rem 0;
        border-bottom: 1px solid #333;
        margin-bottom: 1rem;
    }
    .contact-links a {
        color: #4CAF50;
        text-decoration: none;
        margin: 0 0.5rem;
        font-weight: 500;
        font-family: 'Manrope', sans-serif;
    }
    .contact-links a:hover {
        color: #66BB6A;
        text-decoration: underline;
    }
    .chat-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 0 1rem;
        min-height: 300px;
    }
    .chat-message {
        margin: 0.5rem 0;
        padding: 0.8rem 1.2rem;
        border-radius: 18px;
        max-width: 80%;
        word-wrap: break-word;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: auto;
        text-align: right;
    }
    .assistant-message {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
        color: white;
        margin-right: auto;
    }
    .chat-input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: #1a1a1a;
        padding: 1rem;
        border-top: 1px solid #333;
        z-index: 1000;
    }
    .stChatInput > div > div {
        background: #2d2d2d !important;
        border: 2px solid #4CAF50 !important;
        border-radius: 25px !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        width: 100% !important;
        max-width: 800px !important;
        margin: 0 auto !important;
    }
    .stChatInput > div > div:focus {
        border-color: #66BB6A !important;
        box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.2) !important;
    }
    .stChatInput > div > div::placeholder {
        color: #999 !important;
        font-family: 'Manrope', sans-serif !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 50% !important;
        width: 50px !important;
        height: 50px !important;
        font-size: 1.2rem !important;
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3) !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #66BB6A 0%, #4CAF50 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(76, 175, 80, 0.4) !important;
    }
    .chat-history {
        padding-bottom: 80px;
    }
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700&display=swap');
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🤖 Chat with Ritvik Varghese</h1>
    <p>I'm ritvik, a 3x entrepreneur, most recently sold imagined after scaling it to $400k/revenue. Ask me anything about my journey and work.</p>
    <div class="contact-links">
        <a href="https://ritvik.io">Website</a> | 
        <a href="https://www.linkedin.com/in/rivar/">LinkedIn</a> | 
        <a href="https://x.com/ritvik_varghese">Twitter</a> | 
        <a href="mailto:ritvikvarghese@gmail.com">ritvikvarghese@gmail.com</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Chat container
st.markdown('<div class="chat-container chat-history">', unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages with custom styling
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            {message["content"]}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant-message">
            {message["content"]}
        </div>
        """, unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Ask me anything about my career, work or projects..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message with custom styling
    st.markdown(f"""
    <div class="chat-message user-message">
        {prompt}
    </div>
    """, unsafe_allow_html=True)

    # Get AI response
    response = chat(prompt, st.session_state.messages[:-1])
    
    # Display AI response with custom styling
    st.markdown(f"""
    <div class="chat-message assistant-message">
        {response}
    </div>
    """, unsafe_allow_html=True)

    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

st.markdown('</div>', unsafe_allow_html=True)
