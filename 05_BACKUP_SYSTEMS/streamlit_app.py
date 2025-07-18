#!/usr/bin/env python3
"""
Streamlit Web Interface for Your Personal AI
This creates a beautiful web interface for your AI assistant.

Run with: streamlit run deployment/streamlit_app.py

This demonstrates how AI can help you build AI interfaces:
1. The code structure was designed with AI assistance
2. You can ask AI to add new features to this interface
3. Streamlit makes it easy to deploy AI applications
"""

import streamlit as st
import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import PyPDF2
import requests
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Personal AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

class StreamlitAI:
    def __init__(self):
        self.api_key = os.getenv('HUGGINGFACE_API_KEY') or os.getenv('HUGGINGFACE')
        if self.api_key:
            self.client = InferenceClient(token=self.api_key)
    
    def chat_with_ai(self, messages, model="HuggingFaceH4/zephyr-7b-beta", temperature=0.5):
        """Send messages to AI and get response"""
        if not hasattr(self, 'client'):
            return "❌ Error: Hugging Face API key not configured."
        try:
            response = self.client.chat_completion(
                messages=messages,
                model=model,
                max_tokens=2048,
                temperature=temperature if temperature > 0 else 0.1 # Temp 0 is not allowed
            )
            return response.choices[0].message.content
        except Exception as e:
            print(e)
            if "Model is currently loading" in str(e):
                return "⏳ Model is loading, please try again in a few moments."
            return f"❌ Error: {str(e)}"

def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Load personal info if it exists
    if os.path.exists("personal_info.txt"):
        with open("personal_info.txt", "r", encoding="utf-8") as f:
            st.session_state.personal_info = f.read()
    
    if 'ai_personality' not in st.session_state:
        st.session_state.ai_personality = {
            "name": "Alex",
            "role": "Personal AI Assistant",
            "system_prompt": """You are a helpful, friendly AI assistant. Be natural and conversational in your responses.

- Answer questions accurately and helpfully
- For simple questions like math problems, give direct correct answers
- Be conversational but not overly chatty
- Only mention personal information if the user specifically asks about themselves
- Respond naturally to greetings like "Hello" without revealing personal details"""
        }
    
    if 'conversation_count' not in st.session_state:
        st.session_state.conversation_count = 0

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def fetch_url_content(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup.get_text()
    except Exception as e:
        return f"Error fetching URL: {e}"

def sidebar_controls():
    """Create sidebar with controls and settings"""
    st.sidebar.title("🤖 AI Controls")
    
    # API Key status
    ai = StreamlitAI()
    if hasattr(ai, 'client'):
        st.sidebar.success("✅ API Key Connected")
    else:
        st.sidebar.error("❌ No API Key")
        st.sidebar.info("Add your Hugging Face API key to the .env file")
        
    st.sidebar.markdown("---")
    
    # Personal Information
    st.sidebar.subheader("📄 Personal Information")
    uploaded_files = st.sidebar.file_uploader("Upload .txt or .pdf files", type=["txt", "pdf"], accept_multiple_files=True)
    url_input = st.sidebar.text_input("Or enter a web URL")

    if st.sidebar.button("Load Information"):
        all_text = ""
        if uploaded_files:
            for file in uploaded_files:
                if file.type == "text/plain":
                    all_text += file.read().decode("utf-8") + "\n"
                elif file.type == "application/pdf":
                    all_text += extract_text_from_pdf(file) + "\n"
        
        if url_input:
            all_text += fetch_url_content(url_input) + "\n"

        if all_text:
            st.session_state.personal_info = all_text
            with open("personal_info.txt", "w", encoding="utf-8") as f:
                f.write(all_text)
            st.sidebar.success("Information loaded and saved!")

    if 'personal_info' in st.session_state:
        st.sidebar.text_area("Current Personal Info", st.session_state.personal_info, height=150, disabled=True)
    
    st.sidebar.markdown("---")
    
    # AI Personality Settings
    st.sidebar.subheader("🎭 AI Personality")
    
    new_name = st.sidebar.text_input(
        "AI Name", 
        value=st.session_state.ai_personality["name"]
    )
    
    personality_options = {
        "Helpful Assistant": "You are a helpful, friendly assistant.",
        "Tech Expert": "You are a knowledgeable technology expert.",
        "Creative Partner": "You are a creative partner who loves brainstorming.",
        "Code Mentor": "You are a patient coding mentor and teacher.",
        "Custom": "Enter your own personality..."
    }
    
    personality_type = st.sidebar.selectbox(
        "Personality Type",
        options=list(personality_options.keys())
    )
    
    if personality_type == "Custom":
        custom_prompt = st.sidebar.text_area(
            "Custom System Prompt",
            value=st.session_state.ai_personality["system_prompt"],
            height=100
        )
        system_prompt = custom_prompt
    else:
        system_prompt = personality_options[personality_type]
    
    # Update personality if changed
    if (new_name != st.session_state.ai_personality["name"] or 
        system_prompt != st.session_state.ai_personality["system_prompt"]):
        st.session_state.ai_personality["name"] = new_name
        st.session_state.ai_personality["system_prompt"] = system_prompt
        st.sidebar.success("Personality updated!")
    
    st.sidebar.markdown("---")
    
    # Model Settings
    st.sidebar.subheader("⚙️ Model Settings")
    
    model_choice = st.sidebar.text_input(
        "Hugging Face Model",
        "HuggingFaceH4/zephyr-7b-beta",
        help="Enter a Hugging Face model repository ID."
    )
    
    temperature = st.sidebar.slider(
        "Creativity (Temperature)",
        min_value=0.0,
        max_value=2.0,
        value=0.5,
        step=0.1,
        help="Higher = more creative, Lower = more focused"
    )
    
    st.sidebar.markdown("---")
    
    # Conversation Controls
    st.sidebar.subheader("💬 Conversation")
    
    if st.sidebar.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.conversation_count = 0
        st.rerun()
    
    if st.sidebar.button("💾 Save Chat"):
        save_conversation()
    
    # Stats
    st.sidebar.info(f"Messages: {len(st.session_state.messages)}")
    
    return model_choice, temperature

def save_conversation():
    """Save conversation to file"""
    if not st.session_state.messages:
        st.sidebar.warning("No conversation to save!")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"conversation_{timestamp}.json"
    
    conversation_data = {
        "timestamp": timestamp,
        "ai_personality": st.session_state.ai_personality,
        "messages": st.session_state.messages,
        "message_count": len(st.session_state.messages)
    }
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    with open(f"logs/{filename}", 'w', encoding="utf-8") as f:
        json.dump(conversation_data, f, indent=2)
    
    st.sidebar.success(f"💾 Saved to logs/{filename}")

def display_chat_interface():
    """Display the main chat interface"""
    st.title("🤖 Personal AI Assistant")
    st.markdown(f"**Chat with {st.session_state.ai_personality['name']}** - Your AI built with AI assistance!")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "timestamp" in message:
                st.caption(f"⏰ {message['timestamp']}")
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message
        user_message = {
            "role": "user",
            "content": prompt,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
        st.session_state.messages.append(user_message)
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
            st.caption(f"⏰ {user_message['timestamp']}")
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner(f"{st.session_state.ai_personality['name']} is thinking..."):
                # Prepare messages for AI
                ai = StreamlitAI()
                
                if hasattr(ai, 'client'):
                    # Create a smart system prompt that only uses personal info when relevant
                    base_system_prompt = st.session_state.ai_personality["system_prompt"]
                    
                    # Check if the user is asking about themselves or personal information
                    personal_keywords = [
                        "who am i", "my name", "about me", "my skills", "my education", 
                        "my background", "my experience", "my contact", "my portfolio",
                        "tell me about myself", "what do you know about me"
                    ]
                    
                    user_asking_personal = any(keyword in prompt.lower() for keyword in personal_keywords)
                    
                    if user_asking_personal and 'personal_info' in st.session_state:
                        system_prompt = base_system_prompt + f"\n\nThe user is asking about themselves. Here is their personal information:\n{st.session_state.personal_info}\n\nUse this information to answer their question about themselves."
                    else:
                        system_prompt = base_system_prompt + "\n\nAnswer the user's question naturally and accurately. Do not mention any personal information unless specifically asked."

                    messages_for_ai = [
                        {"role": "system", "content": system_prompt}
                    ]
                    
                    # Add recent conversation history
                    recent_messages = st.session_state.messages[-10:]  # Last 10 messages
                    for msg in recent_messages:
                        messages_for_ai.append({
                            "role": msg["role"],
                            "content": msg["content"]
                        })
                    
                    # Get model settings from sidebar
                    model_choice = st.session_state.get('model_choice', 'HuggingFaceH4/zephyr-7b-beta')
                    temperature = st.session_state.get('temperature', 0.5)
                    
                    # Get AI response
                    response = ai.chat_with_ai(messages_for_ai, model_choice, temperature)
                else:
                    response = """❌ **No API Key Found**
                    
To use this AI assistant, you need to:
1. Get a Hugging Face API key from https://huggingface.co/settings/tokens
2. Add it to your `.env` file as: `HUGGINGFACE=your-key-here`
3. Restart this Streamlit app

**Alternative**: Try the local AI option by running `python local_ai_setup.py`"""
                
                st.markdown(response)
                
                # Add AI response to session state
                ai_message = {
                    "role": "assistant",
                    "content": response,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                }
                st.session_state.messages.append(ai_message)
                st.caption(f"⏰ {ai_message['timestamp']}")
        
        # Update conversation count
        st.session_state.conversation_count += 1

def display_welcome_message():
    """Display welcome message and instructions"""
    if not st.session_state.messages:
        st.markdown(
            """
            <style>
                .stApp {
                    background-color: #1E1E1E;
                    color: #FFFFFF;
                }
                .main {
                    background-color: #1E1E1E;
                }
                .welcome-container {
                    text-align: center;
                    padding: 4rem 2rem;
                }
                .welcome-title {
                    font-size: 3.5rem;
                    font-weight: bold;
                    margin-bottom: 1rem;
                }
                .welcome-subtitle {
                    font-size: 1.5rem;
                    color: #A9A9A9;
                    margin-bottom: 2rem;
                }
                .get-started-button {
                    background-color: #4A90E2;
                    color: white;
                    padding: 1rem 2rem;
                    border-radius: 8px;
                    text-decoration: none;
                    font-weight: bold;
                    font-size: 1.2rem;
                    display: inline-block;
                    margin-bottom: 4rem;
                }
                .features-container {
                    display: flex;
                    justify-content: space-around;
                    flex-wrap: wrap;
                    gap: 2rem;
                }
                .feature-card {
                    background-color: #2C2C2C;
                    padding: 2rem;
                    border-radius: 10px;
                    flex: 1;
                    min-width: 250px;
                    text-align: left;
                }
                .feature-title {
                    font-size: 1.5rem;
                    font-weight: bold;
                    margin-bottom: 1rem;
                }
            </style>
            <div class="welcome-container">
                <h1 class="welcome-title">Your Personal AI Assistant</h1>
                <p class="welcome-subtitle">Built with AI, for you.</p>
                <a href="#chat-interface" class="get-started-button">Get Started</a>
                
                <div class="features-container">
                    <div class="feature-card">
                        <h2 class="feature-title">🤖 Intelligent Chat</h2>
                        <p>Engage in intelligent conversations, ask questions, and get detailed answers.</p>
                    </div>
                    <div class="feature-card">
                        <h2 class="feature-title">🎭 Customizable Personality</h2>
                        <p>Tailor your AI's personality to be a helpful assistant, a tech expert, or anything in between.</p>
                    </div>
                    <div class="feature-card">
                        <h2 class="feature-title">⚙️ Advanced Settings</h2>
                        <p>Fine-tune your AI's performance by adjusting the model and creativity settings.</p>
                    </div>
                </div>
            </div>
            <div id="chat-interface"></div>
            """,
            unsafe_allow_html=True,
        )

def main():
    """Main Streamlit app"""
    # Initialize session state
    initialize_session_state()
    
    # Create sidebar controls and get settings
    model_choice, temperature = sidebar_controls()
    
    # Store settings in session state for use in chat
    st.session_state.model_choice = model_choice
    st.session_state.temperature = temperature
    
    # Display welcome message
    display_welcome_message()
    
    # Display chat interface
    display_chat_interface()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        🤖 Built with AI assistance | Powered by Streamlit & Hugging Face<br>
        <small>This entire interface was created using AI tools to help build AI applications!</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
