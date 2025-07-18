#!/usr/bin/env python3
"""
Simple Personal AI - No Heavy Dependencies Required!
This AI works with just the OpenAI API - no PyTorch needed.
"""

import os
import json
from datetime import datetime

try:
    import openai
    from dotenv import load_dotenv
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class SimplePersonalAI:
    def __init__(self):
        """Initialize your simple personal AI"""
        if not OPENAI_AVAILABLE:
            print("OpenAI package not found. Installing...")
            import subprocess
            import sys
            subprocess.check_call([sys.executable, "-m", "pip", "install", "openai", "python-dotenv"])
            import openai
            from dotenv import load_dotenv
        
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')
        
        if not self.api_key:
            print("No OpenAI API key found.")
            print("   1. Get a key at: https://platform.openai.com/api-keys")
            print("   2. Add it to .env file as: OPENAI_API_KEY=your-key-here")
            print("   3. Or set it now:")
            key = input("   Enter your OpenAI API key (or press Enter to skip): ").strip()
            if key:
                with open('.env', 'w') as f:
                    f.write(f'OPENAI_API_KEY={key}\n')
                self.api_key = key
                print("API key saved to .env file")
        
        if self.api_key:
            openai.api_key = self.api_key
            print("Simple Personal AI ready!")
            print("   Type 'help' for commands, 'quit' to exit")
        else:
            print("Running in demo mode (no API calls)")
    
    def chat(self, message):
        """Chat with your AI"""
        if not self.api_key:
            return "Demo mode: I would respond to: " + message
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful personal AI assistant."},
                    {"role": "user", "content": message}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {e}"
    
    def run(self):
        """Run the chat interface"""
        print("\nChat with your Personal AI:")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['quit', 'exit']:
                    print("\nGoodbye! Your AI is always here when you need it!")
                    break
                elif user_input.lower() == 'help':
                    print("""
                    Available Commands:
                    • Just type normally to chat
                    • 'help' - Show this help
                    • 'quit' - Exit
                    
                    Tips:
                    • Ask me anything!
                    • I can help with coding, writing, analysis, and more
                    • Try: "Help me plan my day" or "Explain quantum physics"
                    """)
                    continue
                
                if not user_input:
                    continue
                
                print(f"\nAI: ", end="")
                response = self.chat(user_input)
                print(response)
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}")

def main():
    """Main function"""
    print("""
    Simple Personal AI
    
    This is a lightweight version that works immediately:
    - No heavy dependencies (PyTorch, etc.)
    - Uses OpenAI API for intelligence
    - Works on any computer
    - Ready in seconds
    
    For advanced features (local AI, web interface), 
    run the full setup after this works.
    """)
    
    ai = SimplePersonalAI()
    ai.run()

if __name__ == "__main__":
    main()
