import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
import os

load_dotenv(override=True)
openai = OpenAI()

# Load data
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

# Simple working version with black and white design
gr.ChatInterface(
    chat,
    type="messages",
    title="Ritvik Varghese",
    description="Ask me about my career, work or projects.",
    examples=[
        "What's your background?",
        "Tell me about your companies", 
        "What are you working on now?",
        "What's your experience with AI?",
        "How did you raise funding?"
    ]
).launch(share=True)