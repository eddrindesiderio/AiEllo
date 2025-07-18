#!/usr/bin/env python3
"""
Streamlit Web App for Your Personal AI (Claude 3.5 Sonnet)
A web interface for your personal AI assistant powered by Claude.

Run with: streamlit run deployment/streamlit_app_claude.py
"""

import streamlit as st
import os
from dotenv import load_dotenv
import anthropic
import asyncio
from datetime import datetime

# Load environment variables
load_dotenv()
load_dotenv(".env")
load_dotenv("../.env")

# Page configuration
st.set_page_config(
    page_title="Personal AI Assistant - Claude Powered",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Claude client
@st.cache_resource
def init_claude_client():
    """Initialize Claude client with caching"""
    claude_api_key = os.getenv("CLAUDE_API_KEY")
    if claude_api_key and claude_api_key != "your_claude_api_key_here":
        try:
            client = anthropic.Anthropic(api_key=claude_api_key)
            # Test the connection
            test_response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=10,
                messages=[{"role": "user", "content": "test"}]
            )
            return client
        except Exception as e:
            st.error(f"Failed to initialize Claude: {e}")
            return None
    return None

# Load personal information
@st.cache_data
def load_personal_info():
    """Load personal information with caching"""
    if os.path.exists("personal_info.txt"):
        with open("personal_info.txt", "r", encoding="utf-8") as f:
            return f.read()
    return ""

# Get system prompt
def get_system_prompt(user_message=""):
    """Get system prompt based on whether user is asking personal questions"""
    personal_info = load_personal_info()
    
    base_prompt = """You are a helpful, friendly AI assistant. Be natural and conversational in your responses.

- Answer questions accurately and helpfully
- For simple questions like math problems, give direct correct answers
- Be conversational but not overly chatty
- Only mention personal information if the user specifically asks about the person
- Respond naturally to greetings like "Hello" without revealing personal details"""
    
    # Check if user is asking about personal information
    personal_keywords = [
        "who am i", "my name", "about me", "my skills", "my education", 
        "my background", "my experience", "my contact", "my portfolio",
        "tell me about myself", "what do you know about me", "eddrin"
    ]
    
    user_asking_personal = any(keyword in user_message.lower() for keyword in personal_keywords)
    
    if user_asking_personal and personal_info:
        return base_prompt + f"\n\nThe user is asking about themselves. Here is their personal information:\n{personal_info}\n\nUse this information to answer their question about themselves."
    else:
        return base_prompt + "\n\nAnswer the user's question naturally and accurately. Do not mention any personal information unless specifically asked."

# Fallback responses
def get_fallback_response(message):
    """Get fallback response when Claude API is not available"""
    message_lower = message.lower()
    personal_info = load_personal_info()
    
    # Check for personal questions
    personal_keywords = [
        "who am i", "my name", "about me", "my skills", "my education", 
        "my background", "my experience", "my contact", "my portfolio",
        "tell me about myself", "what do you know about me", "eddrin"
    ]
    
    if any(keyword in message_lower for keyword in personal_keywords):
        if personal_info:
            return f"Here's what I know about Eddrin Desiderio:\n\n{personal_info}\n\nHe specializes in web development using HTML, CSS, and JavaScript, and is committed to delivering user-friendly solutions."
        else:
            return "Eddrin Desiderio is a web developer with a Bachelor of Science in Information Technology from STI College Tanauan. He specializes in turning design concepts into interactive digital experiences using HTML, CSS, and JavaScript."
    
    # Math questions
    if any(op in message_lower for op in ['+', '-', '*', '/', 'plus', 'minus', 'times', 'divided', '=', 'equals']) or "math" in message_lower:
        if "2+2" in message_lower or "2 + 2" in message_lower:
            return "2 + 2 = 4"
        elif "1+1" in message_lower or "1 + 1" in message_lower:
            return "1 + 1 = 2"
        elif "1+1=" in message_lower or "1 + 1 =" in message_lower:
            return "1 + 1 = 2"
        elif "2+2=" in message_lower or "2 + 2 =" in message_lower:
            return "2 + 2 = 4"
        elif "basic" in message_lower and "math" in message_lower:
            return """Here are basic mathematics concepts:

**Basic Operations:**
- Addition (+): 2 + 3 = 5
- Subtraction (-): 5 - 2 = 3  
- Multiplication (×): 4 × 3 = 12
- Division (÷): 12 ÷ 3 = 4

**Order of Operations (PEMDAS):**
1. Parentheses first
2. Exponents (powers)
3. Multiplication and Division (left to right)
4. Addition and Subtraction (left to right)

**Examples:**
- 2 + 3 × 4 = 2 + 12 = 14
- (2 + 3) × 4 = 5 × 4 = 20

**Fractions:**
- 1/2 = 0.5
- 3/4 = 0.75

What specific math topic would you like help with?"""
        else:
            return "I can help with simple math problems. For complex calculations, I need my Claude API for full functionality."
    
    # Greetings
    if any(greeting in message_lower for greeting in ["hello", "hi", "hey", "good morning", "good afternoon"]):
        return "Hello! I'm your personal AI assistant. How can I help you today?"
    
    # Programming questions
    if any(keyword in message_lower for keyword in ["ai", "artificial intelligence", "code", "coding", "programming", "python", "javascript", "html", "css"]):
        return "I can help with programming and AI concepts! What specific topic would you like to learn about?"
    
    # Default response
    return f"I can help you with '{message}'! I can assist with math problems, programming questions, AI concepts, personal questions about Eddrin, and general information. What would you like to know more about?"

# Main app
def main():
    # Header
    st.title("🤖 Personal AI Assistant")
    st.subheader("Powered by Claude 3.5 Sonnet")
    
    # Initialize Claude client
    claude_client = init_claude_client()
    
    # Sidebar
    with st.sidebar:
        st.header("ℹ️ Information")
        
        if claude_client:
            st.success("✅ Claude API Connected")
            st.info("Using Claude 3.5 Sonnet for intelligent responses")
        else:
            st.error("❌ Claude API Not Connected")
            st.warning("Using fallback responses only")
            
        st.markdown("---")
        st.markdown("### 🎯 What I can help with:")
        st.markdown("""
        - **Math Problems**: Simple calculations and explanations
        - **Programming**: Code help, concepts, best practices
        - **Personal Info**: Ask about Eddrin's background and skills
        - **General Questions**: Wide range of topics
        - **Writing**: Essays, content creation, editing
        - **Learning**: Explanations and tutorials
        """)
        
        st.markdown("---")
        st.markdown("### 💡 Example Questions:")
        st.markdown("""
        - "What is 2+2?"
        - "Tell me about Eddrin"
        - "Explain basic AI concepts"
        - "Help me write a Python function"
        - "What are my skills?"
        """)
    
    # Main chat interface
    st.markdown("---")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                if claude_client:
                    try:
                        # Get system prompt
                        system_prompt = get_system_prompt(prompt)
                        
                        # Call Claude API
                        response = claude_client.messages.create(
                            model="claude-3-5-sonnet-20241022",
                            max_tokens=1000,
                            system=system_prompt,
                            messages=[{"role": "user", "content": prompt}]
                        )
                        ai_response = response.content[0].text
                        
                        # Add debug info if needed
                        if st.session_state.get("debug_mode", False):
                            ai_response = f"🔍 DEBUG: Claude API Success\n\n{ai_response}"
                            
                    except Exception as e:
                        st.error(f"Claude API Error: {e}")
                        ai_response = f"🔧 API Error - using fallback response:\n\n{get_fallback_response(prompt)}"
                else:
                    ai_response = f"🔧 No Claude API - using fallback response:\n\n{get_fallback_response(prompt)}"
                
                st.markdown(ai_response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()
    
    with col2:
        debug_mode = st.checkbox("🔍 Debug Mode", value=st.session_state.get("debug_mode", False))
        st.session_state.debug_mode = debug_mode
    
    with col3:
        st.markdown(f"**Time:** {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()
