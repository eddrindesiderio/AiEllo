#!/usr/bin/env python3
"""
Eddrin's Personal AI Assistant
This AI assistant has knowledge about Eddrin Desiderio and can answer questions accurately
using the provided personal information while also being able to handle general questions.
"""

import os
import json
from dotenv import load_dotenv
import openai
from datetime import datetime

# Load environment variables
load_dotenv()

class EddrinPersonalAI:
    def __init__(self):
        """Initialize Eddrin's personal AI assistant with his information"""
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            print("⚠️  No OpenAI API key found. Please add it to your .env file")
            print("   Get one at: https://platform.openai.com/api-keys")
            return
        
        self.client = openai.OpenAI(api_key=self.api_key)
        self.conversation_history = []
        self.personal_info = self.load_eddrin_info()
        
        print("🤖 Eddrin's Personal AI Assistant initialized!")
        print("   I have knowledge about Eddrin Desiderio and can answer questions accurately")
        print("   Type 'quit' to exit, 'help' for commands")
    
    def load_eddrin_info(self):
        """Load Eddrin's personal information as knowledge base"""
        return {
            "name": "Eddrin Desiderio",
            "education": {
                "degree": "Bachelor of Science in Information Technology",
                "school": "STI College Tanauan",
                "achievement": "Recognized as the best programmer during senior high school years"
            },
            "profession": "Web Developer",
            "specialization": "Turning design concepts into interactive digital experiences",
            "core_technologies": ["HTML", "CSS", "JavaScript"],
            "additional_skills": ["PHP", "MySQL", "Bootstrap", "jQuery", "WordPress"],
            "design_tools": [
                "Adobe Photoshop", "Adobe Illustrator", "Adobe InDesign", 
                "Adobe XD", "Adobe Premiere Pro", "Adobe After Effects",
                "Adobe Audition", "Adobe Lightroom", "VSCO"
            ],
            "development_tools": ["Visual Studio Code", "Adobe Dreamweaver"],
            "marketing_skills": [
                "Google Analytics", "Google Ads", "Google Search Console",
                "Google PageSpeed Insights", "SEO Optimization"
            ],
            "contact": {
                "email": ["eddrin.desiderio@gmail.com", "eddrin.desiderio@outlook.com"],
                "phone": "+63 917-312-759-5858",
                "portfolio": "https://eddrin.netlify.app/"
            },
            "work_philosophy": "Strong focus on delivering user-friendly and custom web solutions that meet client needs on time and within budget",
            "commitment": "Committed to excellence in every aspect of work"
        }
    
    def get_system_prompt(self):
        """Create system prompt with Eddrin's information"""
        return f"""You are an AI assistant with detailed knowledge about Eddrin Desiderio. 

IMPORTANT: When asked about Eddrin Desiderio, use ONLY the following accurate information:

PERSONAL INFO:
- Name: {self.personal_info['name']}
- Education: {self.personal_info['education']['degree']} from {self.personal_info['education']['school']}
- Achievement: {self.personal_info['education']['achievement']}
- Profession: {self.personal_info['profession']}

SKILLS & EXPERTISE:
- Core Technologies: {', '.join(self.personal_info['core_technologies'])}
- Additional Skills: {', '.join(self.personal_info['additional_skills'])}
- Design Tools: {', '.join(self.personal_info['design_tools'])}
- Development Tools: {', '.join(self.personal_info['development_tools'])}
- Marketing Skills: {', '.join(self.personal_info['marketing_skills'])}

SPECIALIZATION: {self.personal_info['specialization']}

WORK PHILOSOPHY: {self.personal_info['work_philosophy']}

CONTACT INFORMATION:
- Email: {' or '.join(self.personal_info['contact']['email'])}
- Phone: {self.personal_info['contact']['phone']}
- Portfolio: {self.personal_info['contact']['portfolio']}

RULES:
1. For questions about Eddrin, use ONLY the information provided above
2. Be accurate and specific when discussing his background, skills, or contact info
3. For general questions not about Eddrin, provide helpful and accurate responses
4. Always maintain a professional and helpful tone
5. If asked about something not in Eddrin's info, clearly state you don't have that specific information about him
"""
    
    def chat(self, user_message):
        """Send message to AI and get response with Eddrin's knowledge"""
        try:
            # Add user message to history
            self.conversation_history.append({
                "role": "user", 
                "content": user_message,
                "timestamp": datetime.now().isoformat()
            })
            
            # Prepare messages for API
            messages = [
                {"role": "system", "content": self.get_system_prompt()}
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
                max_tokens=800,
                temperature=0.3  # Lower temperature for more accurate responses
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
    
    def show_eddrin_info(self):
        """Display Eddrin's information"""
        print(f"""
        👨‍💻 About Eddrin Desiderio:
        
        🎓 Education: {self.personal_info['education']['degree']}
           School: {self.personal_info['education']['school']}
           Achievement: {self.personal_info['education']['achievement']}
        
        💼 Profession: {self.personal_info['profession']}
        🎯 Specialization: {self.personal_info['specialization']}
        
        💻 Core Technologies: {', '.join(self.personal_info['core_technologies'])}
        🔧 Additional Skills: {', '.join(self.personal_info['additional_skills'])}
        
        📧 Contact:
           Email: {' or '.join(self.personal_info['contact']['email'])}
           Phone: {self.personal_info['contact']['phone']}
           Portfolio: {self.personal_info['contact']['portfolio']}
        """)
    
    def test_knowledge(self):
        """Test the AI's knowledge about Eddrin"""
        test_questions = [
            "What is Eddrin's educational background?",
            "What programming languages does Eddrin know?",
            "How can I contact Eddrin?",
            "What is Eddrin's portfolio website?",
            "What achievement did Eddrin receive in school?"
        ]
        
        print("\n🧪 Testing AI Knowledge about Eddrin:")
        print("=" * 50)
        
        for question in test_questions:
            print(f"\n❓ Test Question: {question}")
            response = self.chat(question)
            print(f"🤖 AI Response: {response}")
            print("-" * 30)
    
    def save_conversation(self):
        """Save conversation to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"logs/eddrin_ai_conversation_{timestamp}.json"
        
        os.makedirs("logs", exist_ok=True)
        
        with open(filename, 'w') as f:
            json.dump({
                "personal_info": self.personal_info,
                "conversation": self.conversation_history
            }, f, indent=2)
        
        print(f"💾 Conversation saved to {filename}")
    
    def show_help(self):
        """Show available commands"""
        print("""
        🤖 Eddrin's Personal AI Commands:
        
        • Ask anything about Eddrin Desiderio - I have accurate information!
        • Ask general questions - I can help with other topics too
        • 'info' - Show Eddrin's complete information
        • 'test' - Test my knowledge about Eddrin
        • 'save' - Save conversation to file
        • 'stats' - Show conversation statistics
        • 'clear' - Clear conversation history
        • 'help' - Show this help message
        • 'quit' - Exit the program
        
        💡 Try asking:
        • "What is Eddrin's educational background?"
        • "What skills does Eddrin have?"
        • "How can I contact Eddrin?"
        • "What is Eddrin's portfolio website?"
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
        • Knowledge base: Eddrin Desiderio's personal information
        """)
    
    def run(self):
        """Main chat loop"""
        if not self.api_key:
            return
        
        print(f"\n💬 Chat with Eddrin's Personal AI Assistant:")
        print("Ask me anything about Eddrin Desiderio or general questions!")
        print("=" * 60)
        
        while True:
            try:
                user_input = input("\n🧑 You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() == 'quit':
                    print(f"\n👋 AI: Goodbye! Feel free to contact Eddrin for your web development needs!")
                    break
                elif user_input.lower() == 'help':
                    self.show_help()
                    continue
                elif user_input.lower() == 'info':
                    self.show_eddrin_info()
                    continue
                elif user_input.lower() == 'test':
                    self.test_knowledge()
                    continue
                elif user_input.lower() == 'save':
                    self.save_conversation()
                    continue
                elif user_input.lower() == 'stats':
                    self.show_stats()
                    continue
                elif user_input.lower() == 'clear':
                    self.conversation_history = []
                    print("🗑️  Conversation history cleared!")
                    continue
                
                # Get AI response
                print(f"\n🤖 AI: ", end="")
                response = self.chat(user_input)
                print(response)
                
            except KeyboardInterrupt:
                print(f"\n\n👋 AI: Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")

def main():
    """Main function"""
    print("""
    🚀 Eddrin's Personal AI Assistant
    
    This AI assistant has accurate knowledge about Eddrin Desiderio and can:
    ✅ Answer questions about Eddrin's background, skills, and contact info
    ✅ Provide accurate information based on his personal details
    ✅ Handle general questions on other topics
    ✅ Maintain professional and helpful responses
    
    The AI uses Eddrin's personal information as its knowledge base,
    ensuring accurate and consistent responses about him.
    """)
    
    # Create and run Eddrin's personal AI
    ai = EddrinPersonalAI()
    ai.run()

if __name__ == "__main__":
    main()
