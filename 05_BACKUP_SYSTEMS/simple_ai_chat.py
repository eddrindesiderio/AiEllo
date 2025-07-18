#!/usr/bin/env python3
"""
Simple AI Chatbot - Built with AI Assistance!
This demonstrates how to use AI (OpenAI API) to create your own AI assistant.

This code was generated with AI assistance and shows how you can:
1. Use existing AI APIs to build new AI systems
2. Customize the behavior and personality
3. Add your own features and logic
"""

import os
import json
from dotenv import load_dotenv
import openai
from datetime import datetime

# Load environment variables
load_dotenv()

class PersonalAI:
    def __init__(self):
        """Initialize your personal AI assistant"""
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            print("⚠️  No OpenAI API key found. Please add it to your .env file")
            print("   Get one at: https://platform.openai.com/api-keys")
            return
        
        self.client = openai.OpenAI(api_key=self.api_key)
        self.conversation_history = []
        self.personality = self.load_personality()
        
        print("🤖 Personal AI Assistant initialized!")
        print(f"   Personality: {self.personality['name']}")
        print("   Type 'quit' to exit, 'help' for commands")
    
    def load_personality(self):
        """Load AI personality settings - you can customize this!"""
        return {
            "name": "Alex",
            "role": "Personal AI Assistant",
            "traits": [
                "helpful and friendly",
                "knowledgeable about technology",
                "creative problem solver",
                "good at explaining complex topics simply"
            ],
            "system_prompt": """You are Alex, a personal AI assistant. You are:
            - Helpful, friendly, and encouraging
            - Great at breaking down complex problems
            - Knowledgeable about programming and AI
            - Always ready to help with creative solutions
            
            Remember: You were created by someone learning to build AI with AI assistance!
            Be supportive of their AI development journey."""
        }
    
    def chat(self, user_message):
        """Send message to AI and get response"""
        try:
            # Add user message to history
            self.conversation_history.append({
                "role": "user", 
                "content": user_message,
                "timestamp": datetime.now().isoformat()
            })
            
            # Prepare messages for API
            messages = [
                {"role": "system", "content": self.personality["system_prompt"]}
            ]
            
            # Add recent conversation history (last 10 messages)
            recent_history = self.conversation_history[-10:]
            for msg in recent_history:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Add AI response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": ai_response,
                "timestamp": datetime.now().isoformat()
            })
            
            return ai_response
            
        except Exception as e:
            return f"❌ Error: {str(e)}\nMake sure your API key is valid and you have credits."
    
    def save_conversation(self):
        """Save conversation to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"logs/conversation_{timestamp}.json"
        
        os.makedirs("logs", exist_ok=True)
        
        with open(filename, 'w') as f:
            json.dump({
                "personality": self.personality,
                "conversation": self.conversation_history
            }, f, indent=2)
        
        print(f"💾 Conversation saved to {filename}")
    
    def show_help(self):
        """Show available commands"""
        print("""
        🤖 Personal AI Commands:
        
        • Just type normally to chat with your AI
        • 'help' - Show this help message
        • 'save' - Save conversation to file
        • 'stats' - Show conversation statistics
        • 'personality' - Show AI personality settings
        • 'clear' - Clear conversation history
        • 'quit' - Exit the program
        
        💡 Pro tip: Ask your AI to help you improve this code!
        """)
    
    def show_stats(self):
        """Show conversation statistics"""
        total_messages = len(self.conversation_history)
        user_messages = len([m for m in self.conversation_history if m["role"] == "user"])
        ai_messages = len([m for m in self.conversation_history if m["role"] == "assistant"])
        
        print(f"""
        📊 Conversation Stats:
        • Total messages: {total_messages}
        • Your messages: {user_messages}
        • AI responses: {ai_messages}
        • AI personality: {self.personality['name']}
        """)
    
    def run(self):
        """Main chat loop"""
        if not self.api_key:
            return
        
        print(f"\n💬 Chat with {self.personality['name']} (your personal AI):")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("\n🧑 You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() == 'quit':
                    print(f"\n👋 {self.personality['name']}: Goodbye! Keep building amazing AI!")
                    break
                elif user_input.lower() == 'help':
                    self.show_help()
                    continue
                elif user_input.lower() == 'save':
                    self.save_conversation()
                    continue
                elif user_input.lower() == 'stats':
                    self.show_stats()
                    continue
                elif user_input.lower() == 'personality':
                    print(f"\n🤖 AI Personality: {json.dumps(self.personality, indent=2)}")
                    continue
                elif user_input.lower() == 'clear':
                    self.conversation_history = []
                    print("🗑️  Conversation history cleared!")
                    continue
                
                # Get AI response
                print(f"\n🤖 {self.personality['name']}: ", end="")
                response = self.chat(user_input)
                print(response)
                
            except KeyboardInterrupt:
                print(f"\n\n👋 {self.personality['name']}: Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")

def main():
    """Main function - this is where your AI journey begins!"""
    print("""
    🚀 Welcome to AI Building AI!
    
    This simple chatbot demonstrates how you can use AI to build AI:
    1. We're using OpenAI's API (AI) to create our own AI assistant
    2. You can customize the personality, add features, and make it yours
    3. The best part? You can ask AI tools to help you improve this code!
    
    Try asking your AI assistant:
    • "How can I improve this chatbot?"
    • "Add a feature to remember my preferences"
    • "Help me deploy this as a web app"
    """)
    
    # Create and run your personal AI
    ai = PersonalAI()
    ai.run()

if __name__ == "__main__":
    main()
