#!/usr/bin/env python3
"""
Local AI Setup - No API Keys Required!
This demonstrates how to run AI models locally on your computer.

This approach:
- Uses free, open-source AI models
- Runs entirely on your machine (private)
- No API costs or internet required after initial download
- Can be customized and fine-tuned for your specific needs
"""

import os
try:
    import torch
    from transformers import (
        AutoTokenizer, 
        AutoModelForCausalLM, 
        pipeline,
        Conversation
    )
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    DEPENDENCIES_AVAILABLE = False
    MISSING_DEPENDENCY = str(e)

import warnings
warnings.filterwarnings("ignore")

class LocalAI:
    def __init__(self, model_name="microsoft/DialoGPT-medium"):
        """
        Initialize local AI with a pre-trained model
        
        Popular free models you can try:
        - microsoft/DialoGPT-medium (conversational)
        - microsoft/DialoGPT-large (better but slower)
        - facebook/blenderbot-400M-distill (Facebook's chatbot)
        - microsoft/DialoGPT-small (faster, less capable)
        """
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = None
        self.model = None
        self.chat_history_ids = None
        
        print(f"🤖 Initializing Local AI...")
        print(f"   Model: {model_name}")
        print(f"   Device: {self.device}")
        print(f"   {'GPU acceleration enabled! 🚀' if self.device == 'cuda' else 'Using CPU (slower but works)'}")
        
        self.load_model()
    
    def load_model(self):
        """Load the AI model and tokenizer"""
        try:
            print("\n📥 Loading model (this may take a few minutes first time)...")
            
            # Load tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            
            # Move to GPU if available
            if self.device == "cuda":
                self.model = self.model.to(self.device)
            
            # Add padding token if it doesn't exist
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            print("✅ Model loaded successfully!")
            print("\n💡 Pro tip: This model is now running entirely on your computer!")
            print("   No internet required, completely private, and free to use!")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            print("\n🔧 Troubleshooting:")
            print("   1. Make sure you have internet for the first download")
            print("   2. Try a smaller model like 'microsoft/DialoGPT-small'")
            print("   3. Install required packages: pip install torch transformers")
    
    def chat(self, user_input):
        """Chat with the local AI model"""
        try:
            # Encode user input
            new_user_input_ids = self.tokenizer.encode(
                user_input + self.tokenizer.eos_token, 
                return_tensors='pt'
            )
            
            # Move to device
            if self.device == "cuda":
                new_user_input_ids = new_user_input_ids.to(self.device)
            
            # Append to chat history
            if self.chat_history_ids is not None:
                bot_input_ids = torch.cat([self.chat_history_ids, new_user_input_ids], dim=-1)
            else:
                bot_input_ids = new_user_input_ids
            
            # Generate response
            with torch.no_grad():
                self.chat_history_ids = self.model.generate(
                    bot_input_ids,
                    max_length=1000,
                    num_beams=5,
                    no_repeat_ngram_size=3,
                    do_sample=True,
                    temperature=0.7,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode response
            response = self.tokenizer.decode(
                self.chat_history_ids[:, bot_input_ids.shape[-1]:][0], 
                skip_special_tokens=True
            )
            
            return response.strip()
            
        except Exception as e:
            return f"❌ Error generating response: {e}"
    
    def reset_conversation(self):
        """Reset the conversation history"""
        self.chat_history_ids = None
        print("🗑️  Conversation reset!")
    
    def get_model_info(self):
        """Get information about the loaded model"""
        if self.model is None:
            return "No model loaded"
        
        param_count = sum(p.numel() for p in self.model.parameters())
        return f"""
        🤖 Local AI Model Info:
        • Name: {self.model_name}
        • Parameters: {param_count:,}
        • Device: {self.device}
        • Memory usage: ~{param_count * 4 / 1024**3:.1f} GB
        • Type: Conversational AI
        """

class SimpleLocalChatbot:
    """Alternative simpler approach using Hugging Face pipelines"""
    
    def __init__(self):
        print("🤖 Loading simple local chatbot...")
        try:
            # This is even simpler - uses Hugging Face pipelines
            self.chatbot = pipeline(
                "conversational",
                model="facebook/blenderbot-400M-distill",
                device=0 if torch.cuda.is_available() else -1
            )
            print("✅ Simple chatbot ready!")
        except Exception as e:
            print(f"❌ Error: {e}")
            self.chatbot = None
    
    def chat(self, message):
        """Simple chat interface"""
        if self.chatbot is None:
            return "Chatbot not available"
        
        try:
            conversation = Conversation(message)
            result = self.chatbot(conversation)
            return result.generated_responses[-1]
        except Exception as e:
            return f"Error: {e}"

def demonstrate_local_ai():
    """Demonstrate different local AI approaches"""
    print("""
    🎯 Local AI Demo - Choose your approach:
    
    1. DialoGPT (Microsoft) - Good conversational AI
    2. BlenderBot (Facebook) - Simple pipeline approach
    3. Custom model path - Use your own model
    """)
    
    choice = input("\nEnter choice (1-3) or press Enter for default: ").strip()
    
    if choice == "2":
        print("\n🚀 Using Simple BlenderBot approach...")
        ai = SimpleLocalChatbot()
        
        if ai.chatbot is None:
            print("❌ Could not load simple chatbot")
            return
        
        print("\n💬 Chat with BlenderBot (type 'quit' to exit):")
        while True:
            user_input = input("\n🧑 You: ").strip()
            if user_input.lower() in ['quit', 'exit']:
                break
            
            response = ai.chat(user_input)
            print(f"🤖 Bot: {response}")
    
    elif choice == "3":
        model_name = input("Enter model name (e.g., 'gpt2'): ").strip()
        if not model_name:
            model_name = "gpt2"
        
        print(f"\n🚀 Loading custom model: {model_name}")
        ai = LocalAI(model_name)
        run_chat_loop(ai)
    
    else:
        print("\n🚀 Using DialoGPT (default)...")
        ai = LocalAI()
        run_chat_loop(ai)

def run_chat_loop(ai):
    """Run the main chat loop"""
    if ai.model is None:
        print("❌ Model not loaded properly")
        return
    
    print(ai.get_model_info())
    print("\n💬 Chat with your Local AI (type 'quit' to exit, 'reset' to clear history):")
    print("=" * 60)
    
    while True:
        try:
            user_input = input("\n🧑 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                print("\n👋 Local AI: Goodbye! Your AI ran completely offline! 🔒")
                break
            elif user_input.lower() == 'reset':
                ai.reset_conversation()
                continue
            elif user_input.lower() == 'info':
                print(ai.get_model_info())
                continue
            
            if not user_input:
                continue
            
            print(f"\n🤖 AI: ", end="")
            response = ai.chat(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

def main():
    """Main function"""
    print("""
    🏠 Welcome to Local AI Setup!
    
    This demonstrates how to run AI models locally on your computer:
    
    ✅ Advantages:
    • Completely free (no API costs)
    • Private (runs offline after download)
    • Customizable (you own the model)
    • No internet required after setup
    
    ⚠️  Requirements:
    • Good amount of RAM (4GB+ recommended)
    • Patience for first-time model download
    • GPU optional but recommended for speed
    
    🚀 Let's get started!
    """)
    
    # Check dependencies
    if not DEPENDENCIES_AVAILABLE:
        print(f"""
    ❌ Missing Dependencies Detected!
    
    Error: {MISSING_DEPENDENCY}
    
    🔧 To fix this:
    1. Run the setup script: python setup_ai_project.py
    2. Wait for PyTorch and transformers to install
    3. Then run this script again
    
    💡 The setup script is likely still running and installing dependencies.
    Check your other terminal window!
    """)
        return
    
    # Check system requirements
    print(f"\n🔍 System Check:")
    print(f"   Python: ✅")
    print(f"   PyTorch: {'✅ v' + torch.__version__ if torch.__version__ else '❌'}")
    print(f"   CUDA available: {'✅' if torch.cuda.is_available() else '❌ (CPU only)'}")
    print(f"   RAM: Check task manager - you'll need 4GB+ free")
    
    input("\nPress Enter to continue...")
    
    demonstrate_local_ai()

if __name__ == "__main__":
    main()
