import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
import os

# Set page config FIRST - before any other Streamlit commands
st.set_page_config(
    page_title="Chat with Ritvik",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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

# Custom CSS for the entire app
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Reset and base styles */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Main app styling */
    .stApp {
        background: #0f0f0f !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Hide Streamlit's default elements */
    .stApp > header {
        display: none !important;
    }
    
    .stApp > div[data-testid="stToolbar"] {
        display: none !important;
    }
    
    .stApp > div[data-testid="stDecoration"] {
        display: none !important;
    }
    
    /* Main container */
    .main-container {
        height: 100vh;
        display: flex;
        flex-direction: column;
        background: #0f0f0f;
        max-width: 100%;
        margin: 0 auto;
    }
    
    /* Header section */
    .header-section {
        padding: 1rem 1.5rem;
        background: #0f0f0f;
        border-bottom: 1px solid #2a2a2a;
        flex-shrink: 0;
    }
    
    .header-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.3rem;
        font-family: 'Inter', sans-serif;
    }
    
    .header-subtitle {
        font-size: 0.85rem;
        color: #a0a0a0;
        font-weight: 400;
        font-family: 'Inter', sans-serif;
    }
    
    /* Chat container */
    .chat-container {
        flex: 1;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        background: #0f0f0f;
    }
    
    /* Chat messages area */
    .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 0.5rem 1.5rem;
        background: #0f0f0f;
        scroll-behavior: smooth;
    }
    
    .chat-messages::-webkit-scrollbar {
        width: 6px;
    }
    
    .chat-messages::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    
    .chat-messages::-webkit-scrollbar-thumb {
        background: #404040;
        border-radius: 3px;
    }
    
    .chat-messages::-webkit-scrollbar-thumb:hover {
        background: #555555;
    }
    
    /* Individual message styling */
    .message {
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
    }
    
    .message.user {
        flex-direction: row-reverse;
    }
    
    .message-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.875rem;
        font-weight: 500;
        flex-shrink: 0;
    }
    
    .message.user .message-avatar {
        background: #007bff;
        color: white;
    }
    
    .message.assistant .message-avatar {
        background: #404040;
        color: white;
    }
    
    .message-content {
        max-width: 70%;
        padding: 0.75rem 1rem;
        border-radius: 1rem;
        font-size: 0.95rem;
        line-height: 1.5;
        word-wrap: break-word;
    }
    
    .message.user .message-content {
        background: #007bff;
        color: white;
        border-bottom-right-radius: 0.25rem;
    }
    
    .message.assistant .message-content {
        background: #1a1a1a;
        color: #ffffff;
        border: 1px solid #2a2a2a;
        border-bottom-left-radius: 0.25rem;
    }
    
    /* Input section */
    .input-section {
        padding: 0.75rem 1.5rem 1rem;
        background: #0f0f0f;
        border-top: 1px solid #2a2a2a;
        flex-shrink: 0;
    }
    
    .input-container {
        position: relative;
        display: flex;
        align-items: center;
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 1.5rem;
        padding: 0.75rem 1rem;
        transition: border-color 0.2s ease;
    }
    
    .input-container:focus-within {
        border-color: #007bff;
    }
    
    .input-field {
        flex: 1;
        background: transparent;
        border: none;
        outline: none;
        color: #ffffff;
        font-size: 0.95rem;
        font-family: 'Inter', sans-serif;
        padding: 0.25rem 0.5rem;
    }
    
    .input-field::placeholder {
        color: #666666;
    }
    
    .input-actions {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .send-button {
        background: #007bff;
        border: none;
        border-radius: 50%;
        width: 36px;
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        cursor: pointer;
        transition: background-color 0.2s ease;
    }
    
    .send-button:hover {
        background: #0056b3;
    }
    
    .send-button:disabled {
        background: #404040;
        cursor: not-allowed;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .header-section {
            padding: 0.75rem 1rem;
        }
        
        .header-title {
            font-size: 1.25rem;
        }
        
        .header-subtitle {
            font-size: 0.8rem;
        }
        
        .chat-messages {
            padding: 0.5rem 1rem;
        }
        
        .input-section {
            padding: 0.5rem 1rem 0.75rem;
        }
        
        .message-content {
            max-width: 85%;
        }
    }
    
    /* Hide Streamlit's default chat input */
    .stChatInput {
        display: none !important;
    }
    
    /* Hide Streamlit's default chat messages */
    .stChatMessage {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header
st.markdown("""
<div class="main-container">
    <div class="header-section">
        <div class="header-title">Chat with Ritvik</div>
        <div class="header-subtitle">I'm a 3x entrepreneur who sold Imagined after scaling it to $400k/revenue. Ask me anything about my journey and work.</div>
    </div>
""", unsafe_allow_html=True)

# Chat messages area
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
st.markdown('<div class="chat-messages" id="chat-messages">', unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="message user">
            <div class="message-avatar">U</div>
            <div class="message-content">{message["content"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="message assistant">
            <div class="message-avatar">R</div>
            <div class="message-content">{message["content"]}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close chat-messages

# Input section
st.markdown("""
<div class="input-section">
    <div class="input-container">
        <input type="text" class="input-field" placeholder="Ask anything" id="chat-input">
        <div class="input-actions">
            <button class="send-button" id="send-button">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="22" y1="2" x2="11" y2="13"/>
                    <polygon points="22,2 15,22 11,13 2,9 22,2"/>
                </svg>
            </button>
        </div>
    </div>
</div>
</div>
""", unsafe_allow_html=True)

# JavaScript for handling input
st.markdown("""
<script>
document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-button');
    const chatMessages = document.getElementById('chat-messages');
    
    function sendMessage() {
        const message = input.value.trim();
        if (message) {
            // Add user message to chat
            const userMessageDiv = document.createElement('div');
            userMessageDiv.className = 'message user';
            userMessageDiv.innerHTML = `
                <div class="message-avatar">U</div>
                <div class="message-content">${message}</div>
            `;
            chatMessages.appendChild(userMessageDiv);
            
            // Clear input
            input.value = '';
            
            // Scroll to bottom
            chatMessages.scrollTop = chatMessages.scrollHeight;
            
            // Send to Streamlit
            const event = new CustomEvent('sendMessage', { detail: message });
            window.parent.document.dispatchEvent(event);
        }
    }
    
    sendButton.addEventListener('click', sendMessage);
    
    input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Listen for messages from Streamlit
    window.addEventListener('message', function(event) {
        if (event.data.type === 'assistantMessage') {
            const assistantMessageDiv = document.createElement('div');
            assistantMessageDiv.className = 'message assistant';
            assistantMessageDiv.innerHTML = `
                <div class="message-avatar">R</div>
                <div class="message-content">${event.data.message}</div>
            `;
            chatMessages.appendChild(assistantMessageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    });
});
</script>
""", unsafe_allow_html=True)

# Handle chat input
if prompt := st.chat_input("Ask anything", key="chat_input"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get AI response
    response = chat(prompt, st.session_state.messages[:-1])
    
    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Rerun to update the display
    st.rerun()