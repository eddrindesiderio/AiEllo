#!/usr/bin/env python3
"""
Streamlit Web App for Your Personal AI (BlackBox AI Fixed)
A web interface for your personal AI assistant powered by BlackBox AI with multiple endpoint testing.

Run with: streamlit run deployment/streamlit_app_blackbox_fixed.py
"""

import streamlit as st
import os
from dotenv import load_dotenv
import aiohttp
import asyncio
from datetime import datetime
import json
import time
import requests

# Load environment variables
load_dotenv()
load_dotenv(".env")
load_dotenv("../.env")

# Page configuration
st.set_page_config(
    page_title="Personal AI Assistant - BlackBox AI Fixed",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# BlackBox AI API function with multiple endpoint testing
async def call_blackbox_api(messages, system_prompt=""):
    """Call BlackBox AI API with multiple endpoint attempts"""
    blackbox_api_key = os.getenv("BLACKBOX_API_KEY", "sk-BtiFdMb6OKw95pLEGknfhQ")
    
    if not blackbox_api_key:
        raise Exception("No BlackBox API key found")
    
    # Try multiple possible endpoints and formats
    endpoints_and_formats = [
        # Format 1: Standard OpenAI-style
        {
            "url": "https://api.blackbox.ai/v1/chat/completions",
            "headers": {
                "Authorization": f"Bearer {blackbox_api_key}",
                "Content-Type": "application/json"
            },
            "data": {
                "model": "blackbox",
                "messages": [
                    {"role": "system", "content": system_prompt} if system_prompt else None,
                    {"role": "user", "content": messages[0]["content"]}
                ],
                "max_tokens": 200,
                "temperature": 0.7
            }
        },
        # Format 2: Alternative endpoint
        {
            "url": "https://api.blackbox.ai/chat/completions",
            "headers": {
                "Authorization": f"Bearer {blackbox_api_key}",
                "Content-Type": "application/json"
            },
            "data": {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": messages[0]["content"]}],
                "max_tokens": 200
            }
        },
        # Format 3: Custom BlackBox format (simplified)
        {
            "url": "https://api.blackbox.ai/api/chat",
            "headers": {
                "Authorization": f"Bearer {blackbox_api_key}",
                "Content-Type": "application/json"
            },
            "data": {
                "message": messages[0]["content"],
                "max_tokens": 200
            }
        },
        # Format 4: Direct message format
        {
            "url": "https://blackbox.ai/api/chat",
            "headers": {
                "X-API-Key": blackbox_api_key,
                "Content-Type": "application/json"
            },
            "data": {
                "prompt": messages[0]["content"],
                "max_length": 200
            }
        }
    ]
    
    # Filter out None values from messages
    for config in endpoints_and_formats:
        if "messages" in config["data"]:
            config["data"]["messages"] = [msg for msg in config["data"]["messages"] if msg is not None]
    
    for i, config in enumerate(endpoints_and_formats, 1):
        try:
            st.write(f"🔍 Trying BlackBox AI endpoint {i}: {config['url']}")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    config["url"], 
                    headers=config["headers"], 
                    json=config["data"], 
                    timeout=15
                ) as response:
                    
                    st.write(f"   Status: {response.status}")
                    
                    if response.status == 200:
                        response_text = await response.text()
                        st.write(f"   ✅ Success! Response: {response_text[:100]}...")
                        
                        # Try to parse JSON response
                        try:
                            result = json.loads(response_text)
                            
                            # Handle different response formats
                            if "choices" in result and len(result["choices"]) > 0:
                                return result["choices"][0]["message"]["content"]
                            elif "response" in result:
                                return result["response"]
                            elif "content" in result:
                                return result["content"]
                            elif "text" in result:
                                return result["text"]
                            else:
                                return str(result)
                                
                        except json.JSONDecodeError:
                            # If not JSON, return raw text
                            if response_text.strip():
                                return response_text.strip()
                    
                    else:
                        error_text = await response.text()
                        st.write(f"   ❌ Error {response.status}: {error_text[:100]}")
                        
        except Exception as e:
            st.write(f"   ❌ Exception: {e}")
            continue
    
    raise Exception("All BlackBox AI endpoints failed")

# Synchronous version for Streamlit
def call_blackbox_api_sync(messages, system_prompt=""):
    """Synchronous wrapper for BlackBox AI API"""
    try:
        return asyncio.run(call_blackbox_api(messages, system_prompt))
    except Exception as e:
        raise e

# Initialize BlackBox AI availability
@st.cache_data
def check_blackbox_availability():
    """Check if BlackBox AI API key is available"""
    blackbox_api_key = os.getenv("BLACKBOX_API_KEY", "sk-BtiFdMb6OKw95pLEGknfhQ")
    return blackbox_api_key and blackbox_api_key != "your_blackbox_api_key_here"

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
    """Get fallback response when BlackBox AI API is not available"""
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
            return "I can help with simple math problems. For complex calculations, I need my BlackBox AI API for full functionality."
    
    # Greetings
    if any(greeting in message_lower for greeting in ["hello", "hi", "hey", "good morning", "good afternoon"]):
        return "Hello! I'm your personal AI assistant powered by BlackBox AI. How can I help you today?"
    
    # Programming questions
    if any(keyword in message_lower for keyword in ["ai", "artificial intelligence", "code", "coding", "programming", "python", "javascript", "html", "css"]):
        return "I can help with programming and AI concepts! What specific topic would you like to learn about?"
    
    # Default response
    return f"I can help you with '{message}'! I can assist with math problems, programming questions, AI concepts, personal questions about Eddrin, and general information. What would you like to know more about?"

# Main app
def main():
    # Header
    st.title("🤖 Personal AI Assistant")
    st.subheader("Powered by BlackBox AI (Fixed Version)")
    
    # Check BlackBox AI availability
    blackbox_available = check_blackbox_availability()
    
    # Sidebar
    with st.sidebar:
        st.header("ℹ️ Information")
        
        if blackbox_available:
            st.success("✅ BlackBox AI Key Available")
            st.info("Testing multiple BlackBox AI endpoints for best compatibility")
        else:
            st.error("❌ BlackBox AI Not Available")
            st.warning("Using fallback responses only")
            
        st.markdown("---")
        st.markdown("### 🎯 What I can help with:")
        st.markdown("""
        - **Math Problems**: Simple calculations and explanations
        - **Programming**: Code help, concepts, best practices
        - **Code Generation**: Create HTML, CSS, JavaScript, Python code
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
        - "Create a simple HTML page"
        - "Explain Python basics"
        - "Write a JavaScript function"
        - "What are my skills?"
        """)
        
        st.markdown("---")
        st.markdown("### 🔥 BlackBox AI Fixed Features:")
        st.markdown("""
        - **Multiple Endpoints**: Tests 4 different API endpoints
        - **Multiple Formats**: OpenAI-style, custom, direct message
        - **Smart Fallbacks**: Enhanced local responses
        - **Error Handling**: Graceful degradation
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
            with st.spinner("Testing BlackBox AI endpoints..."):
                if blackbox_available:
                    try:
                        # Get system prompt
                        system_prompt = get_system_prompt(prompt)
                        
                        # Call BlackBox AI API with multiple endpoint testing
                        messages = [{"role": "user", "content": prompt}]
                        ai_response = call_blackbox_api_sync(messages, system_prompt)
                        
                        # Add debug info if needed
                        if st.session_state.get("debug_mode", False):
                            ai_response = f"🔍 DEBUG: BlackBox AI Success\n\n{ai_response}"
                            
                    except Exception as e:
                        st.error(f"BlackBox AI Error: {e}")
                        ai_response = f"🔧 API Error - using fallback response:\n\n{get_fallback_response(prompt)}"
                else:
                    ai_response = f"🔧 No BlackBox AI - using fallback response:\n\n{get_fallback_response(prompt)}"
                
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
    
    # Additional info
    st.markdown("---")
    st.markdown("### 🚀 BlackBox AI Fixed Advantages:")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **✅ Multiple Endpoints:**
        - api.blackbox.ai/v1/chat/completions
        - api.blackbox.ai/chat/completions
        - api.blackbox.ai/api/chat
        - blackbox.ai/api/chat
        """)
    
    with col2:
        st.markdown("""
        **🎯 Multiple Formats:**
        - OpenAI-style requests
        - Custom BlackBox format
        - Direct message format
        - Alternative authentication
        """)

if __name__ == "__main__":
    main()
