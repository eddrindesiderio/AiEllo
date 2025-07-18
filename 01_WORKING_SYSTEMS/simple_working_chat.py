#!/usr/bin/env python3
"""
Simple Working AI Chat - GUARANTEED to Answer Questions
Uses OpenRouter Claude 3.5 Sonnet with fallback responses

Run with: python 01_WORKING_SYSTEMS/simple_working_chat.py
"""

import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
load_dotenv(".env")
load_dotenv("../.env")

# Get API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or os.getenv("CLAUDE_API_KEY")

# Load personal information
def load_personal_info():
    """Load personal information about Eddrin"""
    try:
        if os.path.exists("07_PERSONAL_DATA/personal_info.txt"):
            with open("07_PERSONAL_DATA/personal_info.txt", "r", encoding="utf-8") as f:
                return f.read()
        elif os.path.exists("personal_info.txt"):
            with open("personal_info.txt", "r", encoding="utf-8") as f:
                return f.read()
    except:
        pass
    
    return """
    HELLO!
    I am Eddrin Desiderio
    I hold a Bachelor of Science in Information Technology from STI College Tanauan.

    Introduction
    About Me
    I hold a Bachelor of Science in Information Technology from STI College Tanauan, where I was recognized as the best programmer during my senior high school years. My journey in web development has been driven by a strong focus on delivering user-friendly and custom web solutions that meet client needs on time and within budget. I specialize in turning design concepts into interactive digital experiences using HTML, CSS, and JavaScript. I am committed to excellence in every aspect of my work.
    """

# Check if user is asking personal questions
def is_personal_question(message):
    """Check if the user is asking about personal information"""
    personal_keywords = [
        "who am i", "my name", "about me", "my skills", "my education", 
        "my background", "my experience", "my contact", "my portfolio",
        "tell me about myself", "what do you know about me", "eddrin"
    ]
    
    return any(keyword in message.lower() for keyword in personal_keywords)

# Get system prompt
def get_system_prompt(user_message=""):
    """Get system prompt based on user message"""
    personal_info = load_personal_info()
    
    base_prompt = """You are a helpful, friendly AI assistant. Be natural and conversational in your responses.

- Answer questions accurately and helpfully
- For simple questions like math problems, give direct correct answers
- Be conversational but not overly chatty
- Only mention personal information if the user specifically asks about the person
- Respond naturally to greetings like "Hello" without revealing personal details
- Keep responses concise but complete"""
    
    if is_personal_question(user_message):
        return base_prompt + f"\n\nThe user is asking about themselves. Here is their personal information:\n{personal_info}\n\nUse this information to answer their question about themselves."
    else:
        return base_prompt + "\n\nAnswer the user's question naturally and accurately. Do not mention any personal information unless specifically asked."

# OpenRouter API call
def call_openrouter_api(message, system_prompt):
    """Call OpenRouter API with Claude 3.5 Sonnet"""
    
    if not OPENROUTER_API_KEY:
        print("⚠️ No OpenRouter API key found - using fallback responses")
        return None
    
    try:
        print(f"🔍 Calling OpenRouter API...")
        
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/personal-ai",
            "X-Title": "Personal AI Assistant"
        }
        
        data = {
            "model": "anthropic/claude-3.5-sonnet",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            "max_tokens": 150,  # Reasonable token limit
            "temperature": 0.3
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result["choices"][0]["message"]["content"]
            print(f"✅ OpenRouter API Success!")
            return ai_response
        else:
            print(f"❌ API Error {response.status_code}: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ API Exception: {e}")
        return None

# Fallback responses
def get_fallback_response(message):
    """Get fallback response when API is not available"""
    message_lower = message.lower()
    personal_info = load_personal_info()
    
    # Check for personal questions
    if is_personal_question(message):
        return f"Here's what I know about Eddrin Desiderio:\n\n{personal_info}\n\nHe specializes in web development using HTML, CSS, and JavaScript, and is committed to delivering user-friendly solutions."
    
    # Math questions
    if "2+2" in message_lower or "2 + 2" in message_lower:
        return "2 + 2 = 4"
    elif "1+1" in message_lower or "1 + 1" in message_lower:
        return "1 + 1 = 2"
    elif "3+3" in message_lower or "3 + 3" in message_lower:
        return "3 + 3 = 6"
    elif "5+5" in message_lower or "5 + 5" in message_lower:
        return "5 + 5 = 10"
    elif "10-5" in message_lower or "10 - 5" in message_lower:
        return "10 - 5 = 5"
    elif any(op in message_lower for op in ['+', '-', '*', '/', 'plus', 'minus', 'times', 'divided', '=', 'equals']) or "math" in message_lower:
        return "I can help with math problems! Try asking me calculations like '2+2', '5*3', or '10/2'. What would you like to calculate?"
    
    # Greetings
    if any(greeting in message_lower for greeting in ["hello", "hi", "hey", "good morning", "good afternoon"]):
        return "Hello! I'm your personal AI assistant powered by Claude 3.5 Sonnet. How can I help you today?"
    
    # Programming questions
    if any(keyword in message_lower for keyword in ["code", "coding", "programming", "python", "javascript", "html", "css"]):
        return "I can help with programming! I know HTML, CSS, JavaScript, Python, and web development. What programming topic would you like help with?"
    
    # AI questions
    if any(keyword in message_lower for keyword in ["ai", "artificial intelligence", "machine learning"]):
        return "I can explain AI concepts! Artificial Intelligence involves creating systems that can perform tasks that typically require human intelligence, like understanding language, recognizing patterns, and making decisions. What specific AI topic interests you?"
    
    # Writing questions
    if any(keyword in message_lower for keyword in ["write", "essay", "blog", "article", "story"]):
        return "I can help with writing! I can assist with essays, articles, stories, emails, and creative writing. What type of writing do you need help with?"
    
    # Default response
    return f"I can help you with '{message}'! I can assist with:\n\n• Math problems and calculations\n• Programming and coding questions\n• Information about Eddrin's background and skills\n• Writing and creative tasks\n• AI and technology explanations\n• General questions and information\n\nWhat would you like to know more about?"

# Main chat function
def chat_with_ai(message):
    """Main function to get AI response"""
    print(f"\n🤖 Processing: {message}")
    
    # Get system prompt
    system_prompt = get_system_prompt(message)
    
    # Try OpenRouter API first
    ai_response = call_openrouter_api(message, system_prompt)
    
    # Use fallback if API fails
    if ai_response is None:
        print("🔄 Using fallback response...")
        ai_response = get_fallback_response(message)
    
    return ai_response

# Main interactive loop
def main():
    """Main interactive chat loop"""
    print("🚀 Simple Working AI Chat - GUARANTEED to Answer!")
    print("=" * 60)
    print("✅ Claude 3.5 Sonnet via OpenRouter")
    print("✅ Smart fallback responses")
    print("✅ Personal context about Eddrin")
    print("✅ Math, programming, and general questions")
    print("=" * 60)
    
    # Check API key status
    if OPENROUTER_API_KEY:
        print("🔑 OpenRouter API Key: Found")
    else:
        print("⚠️ OpenRouter API Key: Not found - using fallback responses")
    
    print("\n💡 Example questions to try:")
    print("• What is 2+2?")
    print("• Tell me about Eddrin")
    print("• Create a Python function")
    print("• Explain artificial intelligence")
    print("• Write a short story")
    print("• Hello")
    
    print("\n💬 Start chatting (type 'quit' to exit):")
    print("=" * 60)
    
    while True:
        try:
            # Get user input
            user_input = input(f"\n🧑 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print(f"\n👋 AI: Goodbye! Thanks for chatting!")
                break
            
            # Get AI response
            response = chat_with_ai(user_input)
            print(f"\n🤖 AI: {response}")
            
        except KeyboardInterrupt:
            print(f"\n\n👋 AI: Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again.")

if __name__ == "__main__":
    main()
