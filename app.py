import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv(override=True)
openai = OpenAI()

# Get content from environment variables (secure deployment)
LINKEDIN_CONTENT = os.getenv('LINKEDIN_CONTENT', '')
SUMMARY_CONTENT = os.getenv('SUMMARY_CONTENT', '')

# If not in env vars, fall back to local files (for development only)
if not LINKEDIN_CONTENT and os.path.exists('ask-me/me/linkedin.pdf'):
    from pypdf import PdfReader
    reader = PdfReader('ask-me/me/linkedin.pdf')
    LINKEDIN_CONTENT = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            LINKEDIN_CONTENT += text

if not SUMMARY_CONTENT and os.path.exists('ask-me/me/summary.txt'):
    with open('ask-me/me/summary.txt', 'r', encoding='utf-8') as f:
        SUMMARY_CONTENT = f.read()

name = "Ritvik Varghese"

system_prompt = f"""You are acting as {name}. You are answering questions on {name}'s website, 
particularly questions related to {name}'s career, background, skills and experience. 
Your responsibility is to represent {name} for interactions on the website as faithfully as possible. 
You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. 
Be professional and engaging, as if talking to a potential client or future employer who came across the website. 
If you don't know the answer, say so.

## Summary:
{SUMMARY_CONTENT}

## LinkedIn Profile:
{LINKEDIN_CONTENT}

With this context, please chat with the user, always staying in character as {name}."""

def chat(message, history):
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model="gpt-4o-mini", messages=messages)
    return response.choices[0].message.content

# Streamlit UI
st.set_page_config(page_title="Ritvik Varghese - AI Chat", layout="wide")

st.title("🤖 Chat with Ritvik Varghese")
st.markdown("**Entrepreneur | Product Leader | 3x Founder | Ex-National Athlete**")
st.markdown("Hey there! I'm Ritvik, a serial entrepreneur who's built and scaled companies to $400k+ revenue. Ask me anything about my journey, startups, or what I'm working on next.")

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

# Footer
st.markdown("---")
st.markdown("**Connect with me:** [Website](https://ritvik.io) | [LinkedIn](https://linkedin.com/in/ritvikvarghese) | [Twitter](https://twitter.com/ritvikvarghese) | ritvikvarghese@gmail.com")
