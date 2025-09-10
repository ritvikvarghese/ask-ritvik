
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
import os

# Set page config FIRST - before any other Streamlit commands
st.set_page_config(
    page_title="Chat with Ritvik - AI Entrepreneur Chat",
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

# Add custom HTML head elements using Streamlit's components
st.markdown("""
<script>
// Add meta tags dynamically to the head
const metaTags = [
    {name: 'description', content: 'Chat with Ritvik - 3x entrepreneur who sold Imagined after scaling to $400k revenue. Ask about startups, business, and entrepreneurship.'},
    {name: 'keywords', content: 'Ritvik Varghese, entrepreneur, startup, business, AI chat, Imagined, Ripen, founder'},
    {name: 'author', content: 'Ritvik Varghese'},
    {property: 'og:type', content: 'website'},
    {property: 'og:url', content: 'https://ask.ritvik.io/'},
    {property: 'og:title', content: 'Chat with Ritvik - AI Entrepreneur Chat'},
    {property: 'og:description', content: 'Chat with Ritvik - 3x entrepreneur who sold Imagined after scaling to $400k revenue. Ask about startups, business, and entrepreneurship.'},
    {property: 'og:image', content: 'https://ask.ritvik.io/meta-image.png'},
    {property: 'og:site_name', content: 'Ritvik Varghese'},
    {property: 'twitter:card', content: 'summary_large_image'},
    {property: 'twitter:url', content: 'https://ask.ritvik.io/'},
    {property: 'twitter:title', content: 'Chat with Ritvik - AI Entrepreneur Chat'},
    {property: 'twitter:description', content: 'Chat with Ritvik - 3x entrepreneur who sold Imagined after scaling to $400k revenue. Ask about startups, business, and entrepreneurship.'},
    {property: 'twitter:image', content: 'https://ask.ritvik.io/meta-image.png'},
    {property: 'twitter:creator', content: '@ritvik_varghese'},
    {name: 'robots', content: 'index, follow'},
    {name: 'theme-color', content: '#4CAF50'}
];

metaTags.forEach(tag => {
    const meta = document.createElement('meta');
    if (tag.name) meta.setAttribute('name', tag.name);
    if (tag.property) meta.setAttribute('property', tag.property);
    meta.setAttribute('content', tag.content);
    document.head.appendChild(meta);
});

// Add favicon
const favicon = document.createElement('link');
favicon.rel = 'icon';
favicon.type = 'image/png';
favicon.href = 'https://ask.ritvik.io/robot-favicon.png';
document.head.appendChild(favicon);
</script>
""", unsafe_allow_html=True)

# Streamlit UI with Mobile-First Responsive Design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700&display=swap');
    
    /* Global Mobile-First Styles */
    * {
        box-sizing: border-box;
    }
    
    /* Force dark theme on all elements */
    .main .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        max-width: 100% !important;
    }
    
    /* Override Streamlit's default white background */
    .stApp {
        background-color: #0e1117 !important;
        color: white !important;
    }
    
    .stApp > header {
        background-color: #0e1117 !important;
    }
    
    .stApp > div {
        background-color: #0e1117 !important;
    }
    
    /* Header Styles - Mobile First */
    .main-header {
        text-align: center;
        padding: 0.5rem 0.3rem;
        margin-bottom: 0.3rem;
        background: #0e1117;
    }
    
    .main-header h1 {
        color: #fff !important;
        font-size: 1.8rem;
        margin-bottom: 0.3rem;
        font-family: 'Manrope', sans-serif;
        font-weight: 700;
    }
    
    .main-header p {
        color: #ccc !important;
        font-size: 0.9rem;
        margin: 0 0 0.5rem 0;
        font-family: 'Manrope', sans-serif;
        line-height: 1.4;
        padding: 0 0.5rem;
    }
    
    .contact-links {
        text-align: center;
        padding: 0.3rem 0.3rem;
        border-bottom: 1px solid #333;
        margin-bottom: 0.5rem;
        background: #0e1117;
    }
    
    .contact-links a {
        color: #007bff !important;
        text-decoration: none;
        margin: 0 0.3rem;
        font-weight: 500;
        font-family: 'Manrope', sans-serif;
        font-size: 0.85rem;
        display: inline-block;
        padding: 0.2rem 0;
    }
    
    .contact-links a:hover {
        color: #0056b3 !important;
        text-decoration: underline;
    }
    
    /* Chat Container - Mobile Responsive */
    .chat-container {
        max-width: 100%;
        margin: 0 auto;
        padding: 0 0.5rem;
        min-height: 250px;
        background: #0e1117;
    }
    
    .chat-message {
        margin: 0.4rem 0;
        padding: 0.7rem 1rem;
        border-radius: 15px;
        max-width: 85%;
        word-wrap: break-word;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        font-size: 0.9rem;
        line-height: 1.4;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        margin-left: auto;
        text-align: right;
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
        color: white !important;
        margin-right: auto;
    }
    
    /* Chat Input - Mobile Optimized */
    .stChatInput {
        background: #0e1117 !important;
        padding: 0.5rem !important;
        border-top: 1px solid #333 !important;
        position: relative !important;
        z-index: 10 !important;
    }
    
    .stChatInput > div > div {
        background: #2d2d2d !important;
        border: 2px solid #ffffff !important;
        border-radius: 20px !important;
        padding: 0.6rem 1rem !important;
        font-size: 0.9rem !important;
        width: 100% !important;
        margin: 0 !important;
        color: white !important;
        -webkit-appearance: none !important;
        -moz-appearance: none !important;
        appearance: none !important;
    }
    
    .stChatInput > div > div:focus {
        border-color: #ffffff !important;
        box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.3) !important;
        outline: none !important;
        background: #2d2d2d !important;
    }
    
    .stChatInput > div > div::placeholder {
        color: #999 !important;
        font-family: 'Manrope', sans-serif !important;
    }
    
    /* Force dark background on all input elements */
    input[type="text"], input[type="search"], textarea {
        background-color: #2d2d2d !important;
        color: white !important;
        border: 2px solid #4CAF50 !important;
        -webkit-appearance: none !important;
        -moz-appearance: none !important;
        appearance: none !important;
    }
    
    input[type="text"]:focus, input[type="search"]:focus, textarea:focus {
        background-color: #2d2d2d !important;
        color: white !important;
        border-color: #66BB6A !important;
        outline: none !important;
    }
    
    /* Override Streamlit's default input styling */
    .stTextInput > div > div > input {
        background-color: #2d2d2d !important;
        color: white !important;
        border: 2px solid #4CAF50 !important;
        border-radius: 20px !important;
        -webkit-appearance: none !important;
        -moz-appearance: none !important;
        appearance: none !important;
    }
    
    .stTextInput > div > div > input:focus {
        background-color: #2d2d2d !important;
        color: white !important;
        border-color: #66BB6A !important;
        box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2) !important;
    }
    
    /* Mobile-specific input fixes */
    @media (max-width: 768px) {
        .stChatInput {
            background: #0e1117 !important;
            padding: 0.8rem 0.5rem !important;
            border-top: 1px solid #333 !important;
        }
        
        .stChatInput > div > div {
            background: #2d2d2d !important;
            color: white !important;
            border: 2px solid #4CAF50 !important;
            -webkit-appearance: none !important;
            -moz-appearance: none !important;
            appearance: none !important;
            font-size: 16px !important; /* Prevents zoom on iOS */
        }
        
        input[type="text"], input[type="search"] {
            background-color: #2d2d2d !important;
            color: white !important;
            -webkit-appearance: none !important;
            -moz-appearance: none !important;
            appearance: none !important;
        }
        
        /* Ensure chat history has proper spacing */
        .chat-history {
            padding-bottom: 100px !important;
        }
    }
    
    /* Additional mobile fixes for input styling */
    @media (max-width: 480px) {
        .stChatInput > div > div {
            font-size: 16px !important;
            padding: 0.8rem 1rem !important;
        }
    }
    
    /* Send Button - Mobile Friendly */
    .stButton > button {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 50% !important;
        width: 45px !important;
        height: 45px !important;
        font-size: 1rem !important;
        box-shadow: 0 3px 10px rgba(76, 175, 80, 0.3) !important;
        margin-left: 0.5rem !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #66BB6A 0%, #4CAF50 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4) !important;
    }
    
    .chat-history {
        padding-bottom: 80px;
        background: #0e1117;
        min-height: calc(100vh - 200px);
    }
    
    /* Ensure proper spacing on mobile */
    @media (max-width: 768px) {
        .chat-history {
            padding-bottom: 100px !important;
            min-height: calc(100vh - 200px) !important;
        }
    }
    
    /* Tablet Styles */
    @media (min-width: 768px) {
        .main-header h1 {
            font-size: 2.2rem;
        }
        
        .main-header p {
            font-size: 1rem;
        }
        
        .chat-container {
            max-width: 800px;
            padding: 0 1rem;
        }
        
        .chat-message {
            max-width: 80%;
            padding: 0.8rem 1.2rem;
            font-size: 1rem;
        }
        
        .contact-links a {
            margin: 0 0.5rem;
            font-size: 0.9rem;
        }
    }
    
    /* Desktop Styles */
    @media (min-width: 1024px) {
        .main-header h1 {
            font-size: 2.5rem;
        }
        
        .main-header p {
            font-size: 1.1rem;
        }
        
        .chat-container {
            max-width: 900px;
        }
        
        .chat-message {
            max-width: 75%;
        }
        
        .stChatInput > div > div {
            font-size: 1rem;
            padding: 0.75rem 1rem;
        }
    }
    
    /* Ensure all text is visible on dark background */
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: white !important;
    }
    
    /* Fix any white backgrounds */
    .stChatMessage {
        background-color: transparent !important;
    }
    
    .stChatMessage[data-testid="user-message"] {
        background-color: transparent !important;
    }
    
    .stChatMessage[data-testid="assistant-message"] {
        background-color: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🤖 Chat with Ritvik</h1>
    <p>I'm ritvik, a 3x entrepreneur, most recently sold imagined after scaling it to $400k/revenue.</p>
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

# Suggested questions removed
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
