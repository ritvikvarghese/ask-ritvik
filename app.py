import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
import os

load_dotenv(override=True)

# Initialize OpenAI client with error handling
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("OPENAI_API_KEY environment variable not set")
    openai = None
else:
    try:
        openai = OpenAI(api_key=api_key)
        print("OpenAI client initialized successfully")
    except Exception as e:
        print(f"OpenAI API error: {e}")
        openai = None

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
    if openai is None:
        return "Sorry, the AI service is not available. Please check the API configuration."
    
    try:
        messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
        response = openai.chat.completions.create(model="gpt-4o-mini", messages=messages)
        return response.choices[0].message.content
    except Exception as e:
        return f"Sorry, there was an error: {str(e)}"

# Create and launch the Gradio interface
demo = gr.ChatInterface(
    chat,
    type="messages",
    title="ritvik varghese",
    description="sk me about my career, work or projects.",
    examples=[
        "introduce yourself",
        "tell me about your companies", 
        "what are your skills?", 
        "tell me about your latest company",
        "what's your work experience?",
        "what projects have you worked on?"
    ],
    css="""
    .gradio-container {
        text-align: center !important;
    }
    .gradio-container h1 {
        text-align: center !important;
        font-size: 2.5rem !important;
        margin-bottom: 1rem !important;
    }
    .gradio-container p {
        text-align: center !important;
        font-size: 1.2rem !important;
        margin-bottom: 2rem !important;
    }
    /* Left align chat messages */
    .message-wrap {
        text-align: left !important;
    }
    .message {
        text-align: left !important;
    }
    .chat-message {
        text-align: left !important;
    }
    .bot-message {
        text-align: left !important;
    }
    .user-message {
        text-align: left !important;
    }
    /* Target Gradio's specific message classes */
    .message-wrap .message {
        text-align: left !important;
    }
    .message-wrap .message .markdown {
        text-align: left !important;
    }
    .message-wrap .message .markdown p {
        text-align: left !important;
    }
    /* Target the actual message content */
    .message-wrap .message .markdown * {
        text-align: left !important;
    }
    /* Fix auto-scroll behavior */
    .gradio-container .chat-container {
        scroll-behavior: auto !important;
    }
    .gradio-container .chat-container .overflow-y-auto {
        scroll-behavior: auto !important;
    }
    /* Prevent auto-scroll to bottom */
    .gradio-container .chat-container .overflow-y-auto::-webkit-scrollbar {
        width: 6px;
    }
    .gradio-container .chat-container .overflow-y-auto::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 3px;
    }
    .gradio-container .chat-container .overflow-y-auto::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 3px;
    }
    .gradio-container .chat-container .overflow-y-auto::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
    """
)

if __name__ == "__main__":
    # Railway configuration
    port = int(os.environ.get("PORT", 8080))
    
    # Add custom JavaScript to control scrolling
    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=True,  # Enable share for public access
        js="""
        // Prevent auto-scroll to bottom
        document.addEventListener('DOMContentLoaded', function() {
            const chatContainer = document.querySelector('.chat-container .overflow-y-auto');
            if (chatContainer) {
                // Disable smooth scrolling
                chatContainer.style.scrollBehavior = 'auto';
                
                // Prevent auto-scroll on new messages
                const observer = new MutationObserver(function(mutations) {
                    mutations.forEach(function(mutation) {
                        if (mutation.type === 'childList') {
                            // Don't auto-scroll, let user control
                            return;
                        }
                    });
                });
                
                observer.observe(chatContainer, {
                    childList: true,
                    subtree: true
                });
            }
        });
        """
    )