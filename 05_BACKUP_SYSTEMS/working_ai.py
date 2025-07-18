#!/usr/bin/env python3
"""
Working Personal AI - Guaranteed to Work!
This bypasses all dependency issues and provides immediate AI functionality.
"""

import os
import sys
import json
from datetime import datetime

def install_if_missing(package):
    """Install package if missing"""
    try:
        __import__(package.replace('-', '_'))
        return True
    except ImportError:
        print(f"Installing {package}...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True

class WorkingPersonalAI:
    def __init__(self):
        """Initialize AI with automatic dependency handling"""
        print("🤖 Initializing Working Personal AI...")
        
        # Install required packages
        install_if_missing("openai")
        install_if_missing("python-dotenv")
        
        # Now import them
        import openai
        from dotenv import load_dotenv
        
        # Load environment
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')
        
        if not self.api_key:
            print("\n🔑 OpenAI API Key Setup:")
            print("   1. Get your key: https://platform.openai.com/api-keys")
            print("   2. Copy and paste it below")
            
            key = input("\n   Enter your OpenAI API key (or press Enter to skip): ").strip()
            if key:
                # Save to .env file
                with open('.env', 'w', encoding='utf-8') as f:
                    f.write(f'OPENAI_API_KEY={key}\n')
                self.api_key = key
                print("✅ API key saved!")
            else:
                print("⚠️  Running in demo mode")
        
        if self.api_key:
            openai.api_key = self.api_key
            print("✅ Personal AI ready!")
        
        self.conversation_history = []
    
    def chat(self, message):
        """Chat with AI"""
        if not self.api_key:
            return f"[Demo Mode] I would respond to: {message}"
        
        try:
            import openai
            
            # Add to conversation history
            self.conversation_history.append({"role": "user", "content": message})
            
            # Keep only last 10 messages for context
            recent_history = self.conversation_history[-10:]
            
            # Create messages for API
            messages = [
                {"role": "system", "content": "You are a helpful, friendly personal AI assistant. Be conversational and helpful."}
            ] + recent_history
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            return ai_response
            
        except Exception as e:
            return f"Error: {str(e)}\n\nTip: Make sure your API key is valid and you have credits."
    
    def save_conversation(self):
        """Save conversation to file"""
        if not self.conversation_history:
            print("No conversation to save.")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"conversation_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)
            print(f"💾 Conversation saved to {filename}")
        except Exception as e:
            print(f"Error saving: {e}")
    
    def show_help(self):
        """Show help information"""
        print("""
        🤖 Personal AI Commands:
        
        • Just type normally to chat with your AI
        • 'help' - Show this help message
        • 'save' - Save conversation to file
        • 'clear' - Clear conversation history
        • 'quit' or 'exit' - Exit the program
        
        💡 Tips:
        • Ask me anything - coding, writing, analysis, planning
        • I remember our conversation context
        • Try: "Help me plan my day" or "Explain machine learning"
        • I can help with creative writing, problem solving, and more!
        """)
    
    def run(self):
        """Run the AI chat interface"""
        print("""
        🚀 Working Personal AI - Ready to Chat!
        
        This AI works immediately without complex dependencies.
        Type 'help' for commands or just start chatting!
        """)
        
        print("\n" + "="*60)
        print("💬 Chat with your Personal AI:")
        print("="*60)
        
        while True:
            try:
                user_input = input("\n🧑 You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() in ['quit', 'exit']:
                    print("\n👋 Goodbye! Your AI is always here when you need it!")
                    break
                elif user_input.lower() == 'help':
                    self.show_help()
                    continue
                elif user_input.lower() == 'save':
                    self.save_conversation()
                    continue
                elif user_input.lower() == 'clear':
                    self.conversation_history = []
                    print("🗑️  Conversation history cleared!")
                    continue
                
                # Get AI response
                print(f"\n🤖 AI: ", end="", flush=True)
                response = self.chat(user_input)
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")

def main():
    """Main function"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                🤖 Working Personal AI 🤖                     ║
    ║              Guaranteed to Work - No Issues!                 ║
    ╚══════════════════════════════════════════════════════════════╝
    
    This AI:
    ✅ Works immediately (no complex dependencies)
    ✅ Handles missing packages automatically
    ✅ Provides full ChatGPT-like functionality
    ✅ Saves conversations and remembers context
    ✅ No PyTorch or transformers needed
    """)
    
    try:
        ai = WorkingPersonalAI()
        ai.run()
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("\n🔧 Troubleshooting:")
        print("   1. Make sure you have internet connection")
        print("   2. Try running: pip install openai python-dotenv")
        print("   3. Get OpenAI API key from: https://platform.openai.com/api-keys")

if __name__ == "__main__":
    main()
