
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

# Streamlit UI with Chat Styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        border-bottom: 1px solid #333;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: #fff;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .main-header p {
        color: #ccc;
        font-size: 1.1rem;
        margin: 0;
    }
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 0 1rem;
    }
    .footer {
        text-align: center;
        padding: 2rem 0;
        border-top: 1px solid #333;
        margin-top: 2rem;
        color: #ccc;
    }
    .stChatMessage {
        background-color: #1e1e1e;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .stChatMessage[data-testid="user-message"] {
        background-color: #2d2d2d;
    }
    .stChatMessage[data-testid="assistant-message"] {
        background-color: #1e1e1e;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🤖 Chat with Ritvik Varghese</h1>
    <p>I'm ritvik, a 3x entrepreneur, most recently sold imagined after scaling it to $400k/revenue. Ask me anything about my journey and work.</p>
</div>
""", unsafe_allow_html=True)

# Chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about my career, work or projects..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        response = chat(prompt, st.session_state.messages[:-1])
        st.markdown(response)

    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <strong>Connect with me:</strong> <a href="https://ritvik.io" style="color: #4CAF50;">Website</a> | 
    <a href="https://linkedin.com/in/ritvikvarghese" style="color: #4CAF50;">LinkedIn</a> | 
    <a href="https://twitter.com/ritvikvarghese" style="color: #4CAF50;">Twitter</a> | 
    <a href="mailto:ritvikvarghese@gmail.com" style="color: #4CAF50;">ritvikvarghese@gmail.com</a>
</div>
""", unsafe_allow_html=True)
