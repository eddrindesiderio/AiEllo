#!/usr/bin/env python3
"""
Personal AI Assistant Example
This shows how to create a comprehensive personal assistant using AI.

Features:
- Task management
- Calendar integration
- Email drafting
- Research assistance
- Code help
- Creative writing

Built with AI assistance to demonstrate AI building AI!
"""

import os
import json
import openai
from datetime import datetime, timedelta
from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import AIConfig, get_personality

load_dotenv()

class PersonalAssistant:
    """A comprehensive personal AI assistant"""
    
    def __init__(self, name="PersonalAI"):
        self.name = name
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.personality = get_personality("Helpful Assistant")
        self.tasks = []
        self.notes = []
        self.conversation_history = []
        
        if self.api_key:
            openai.api_key = self.api_key
        
        print(f"🤖 {self.name} Personal Assistant initialized!")
        print(f"   Personality: {self.personality['name']}")
        print("   Available commands: help, task, note, research, code, write, schedule")
    
    def chat(self, message, context="general"):
        """Main chat interface with context awareness"""
        if not self.api_key or self.api_key == "your-openai-api-key-here":
            return "❌ Please configure your OpenAI API key in the .env file"
        
        # Build context-aware system prompt
        system_prompt = f"""
        {self.personality['system_prompt']}
        
        Context: {context}
        Current date/time: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        
        You have access to the user's:
        - Tasks: {len(self.tasks)} items
        - Notes: {len(self.notes)} items
        - Recent conversations: {len(self.conversation_history)} messages
        
        Be helpful, personal, and context-aware in your responses.
        """
        
        # Prepare messages
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add recent conversation history
        recent_history = self.conversation_history[-5:]
        for msg in recent_history:
            messages.append(msg)
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        try:
            response = openai.ChatCompletion.create(
                model=AIConfig.DEFAULT_MODEL,
                messages=messages,
                max_tokens=AIConfig.MAX_TOKENS,
                temperature=self.personality.get('temperature', AIConfig.TEMPERATURE)
            )
            
            ai_response = response.choices[0].message.content
            
            # Store conversation
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            return ai_response
            
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def manage_tasks(self, action, task_description=None):
        """Task management system"""
        if action == "add" and task_description:
            task = {
                "id": len(self.tasks) + 1,
                "description": task_description,
                "created": datetime.now().isoformat(),
                "completed": False,
                "priority": "medium"
            }
            self.tasks.append(task)
            return f"✅ Added task: {task_description}"
        
        elif action == "list":
            if not self.tasks:
                return "📝 No tasks found"
            
            task_list = "📝 Your Tasks:\n"
            for task in self.tasks:
                status = "✅" if task["completed"] else "⏳"
                task_list += f"{status} {task['id']}. {task['description']}\n"
            return task_list
        
        elif action == "complete" and task_description:
            try:
                task_id = int(task_description)
                for task in self.tasks:
                    if task["id"] == task_id:
                        task["completed"] = True
                        return f"✅ Completed task: {task['description']}"
                return f"❌ Task {task_id} not found"
            except ValueError:
                return "❌ Please provide a valid task ID"
        
        elif action == "smart_add":
            # Use AI to parse and categorize the task
            ai_response = self.chat(f"Parse this task and suggest priority and category: {task_description}", "task_management")
            self.manage_tasks("add", task_description)
            return f"✅ Smart task added with AI analysis:\n{ai_response}"
        
        return "❌ Invalid task action. Use: add, list, complete, smart_add"
    
    def take_notes(self, action, note_content=None):
        """Note-taking system"""
        if action == "add" and note_content:
            note = {
                "id": len(self.notes) + 1,
                "content": note_content,
                "timestamp": datetime.now().isoformat(),
                "tags": []
            }
            
            # Use AI to suggest tags
            tag_suggestion = self.chat(f"Suggest 2-3 relevant tags for this note: {note_content}", "note_tagging")
            
            self.notes.append(note)
            return f"📝 Note added!\n💡 AI suggests tags: {tag_suggestion}"
        
        elif action == "list":
            if not self.notes:
                return "📝 No notes found"
            
            notes_list = "📝 Your Notes:\n"
            for note in self.notes[-5:]:  # Show last 5 notes
                timestamp = datetime.fromisoformat(note["timestamp"]).strftime("%m/%d %H:%M")
                notes_list += f"{note['id']}. [{timestamp}] {note['content'][:50]}...\n"
            return notes_list
        
        elif action == "search" and note_content:
            # Search notes using AI
            search_prompt = f"Search through these notes for: {note_content}\n\nNotes: {json.dumps(self.notes, indent=2)}"
            return self.chat(search_prompt, "note_search")
        
        return "❌ Invalid note action. Use: add, list, search"
    
    def research_assistant(self, topic):
        """AI-powered research assistant"""
        research_prompt = f"""
        Research the topic: {topic}
        
        Provide:
        1. Key points and overview
        2. Important facts and statistics
        3. Recent developments
        4. Useful resources and links
        5. Practical applications
        
        Make it comprehensive but easy to understand.
        """
        
        return self.chat(research_prompt, "research")
    
    def code_helper(self, request):
        """Programming assistance"""
        code_prompt = f"""
        Programming request: {request}
        
        Please provide:
        1. Clear explanation of the solution
        2. Well-commented code example
        3. Best practices and tips
        4. Common pitfalls to avoid
        
        Focus on clean, readable, and efficient code.
        """
        
        return self.chat(code_prompt, "programming")
    
    def creative_writer(self, request):
        """Creative writing assistance"""
        writing_prompt = f"""
        Creative writing request: {request}
        
        Be creative, engaging, and original. Consider:
        1. Tone and style appropriate for the request
        2. Vivid descriptions and imagery
        3. Compelling narrative or structure
        4. Emotional resonance
        """
        
        return self.chat(writing_prompt, "creative_writing")
    
    def schedule_helper(self, request):
        """Schedule and calendar assistance"""
        schedule_prompt = f"""
        Schedule request: {request}
        Current date/time: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        
        Help with:
        1. Time management suggestions
        2. Schedule optimization
        3. Reminder setting
        4. Priority planning
        
        Be practical and considerate of work-life balance.
        """
        
        return self.chat(schedule_prompt, "scheduling")
    
    def process_command(self, user_input):
        """Process user commands and route to appropriate functions"""
        input_lower = user_input.lower().strip()
        
        if input_lower.startswith("task "):
            parts = user_input[5:].split(" ", 1)
            action = parts[0]
            description = parts[1] if len(parts) > 1 else None
            return self.manage_tasks(action, description)
        
        elif input_lower.startswith("note "):
            parts = user_input[5:].split(" ", 1)
            action = parts[0]
            content = parts[1] if len(parts) > 1 else None
            return self.take_notes(action, content)
        
        elif input_lower.startswith("research "):
            topic = user_input[9:]
            return self.research_assistant(topic)
        
        elif input_lower.startswith("code "):
            request = user_input[5:]
            return self.code_helper(request)
        
        elif input_lower.startswith("write "):
            request = user_input[6:]
            return self.creative_writer(request)
        
        elif input_lower.startswith("schedule "):
            request = user_input[9:]
            return self.schedule_helper(request)
        
        elif input_lower == "help":
            return self.show_help()
        
        elif input_lower in ["status", "summary"]:
            return self.get_status_summary()
        
        else:
            # General conversation
            return self.chat(user_input)
    
    def show_help(self):
        """Show available commands"""
        return """
        🤖 Personal AI Assistant Commands:
        
        📋 Task Management:
        • task add [description] - Add a new task
        • task list - Show all tasks
        • task complete [id] - Mark task as complete
        • task smart_add [description] - Add task with AI analysis
        
        📝 Notes:
        • note add [content] - Add a new note
        • note list - Show recent notes
        • note search [query] - Search through notes
        
        🔍 Research:
        • research [topic] - Get comprehensive research on any topic
        
        💻 Programming:
        • code [request] - Get programming help and code examples
        
        ✍️ Writing:
        • write [request] - Get creative writing assistance
        
        📅 Scheduling:
        • schedule [request] - Get help with time management
        
        📊 General:
        • status - Get summary of tasks, notes, and activity
        • help - Show this help message
        
        💬 Or just chat normally for general assistance!
        """
    
    def get_status_summary(self):
        """Get a summary of current status"""
        pending_tasks = len([t for t in self.tasks if not t["completed"]])
        completed_tasks = len([t for t in self.tasks if t["completed"]])
        
        summary = f"""
        📊 Personal Assistant Status:
        
        📋 Tasks:
        • Pending: {pending_tasks}
        • Completed: {completed_tasks}
        • Total: {len(self.tasks)}
        
        📝 Notes: {len(self.notes)} items
        💬 Conversations: {len(self.conversation_history)} messages
        
        🕐 Current time: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        
        Ready to help with your next request! 🚀
        """
        
        return summary
    
    def save_data(self):
        """Save assistant data to file"""
        data = {
            "tasks": self.tasks,
            "notes": self.notes,
            "conversation_history": self.conversation_history[-50:],  # Keep last 50 messages
            "timestamp": datetime.now().isoformat()
        }
        
        os.makedirs("data", exist_ok=True)
        with open("data/personal_assistant_data.json", "w") as f:
            json.dump(data, f, indent=2)
        
        return "💾 Data saved successfully!"
    
    def load_data(self):
        """Load assistant data from file"""
        try:
            with open("data/personal_assistant_data.json", "r") as f:
                data = json.load(f)
            
            self.tasks = data.get("tasks", [])
            self.notes = data.get("notes", [])
            self.conversation_history = data.get("conversation_history", [])
            
            return "📂 Data loaded successfully!"
        except FileNotFoundError:
            return "📂 No saved data found - starting fresh!"
        except Exception as e:
            return f"❌ Error loading data: {e}"

def main():
    """Main function to run the personal assistant"""
    print("""
    🤖 Welcome to Your Personal AI Assistant!
    
    This is a comprehensive AI assistant built with AI assistance.
    It can help you with:
    
    • Task management and productivity
    • Note-taking and organization  
    • Research and information gathering
    • Programming and technical help
    • Creative writing and brainstorming
    • Schedule and time management
    
    Type 'help' for commands or just chat naturally!
    """)
    
    # Create assistant
    assistant = PersonalAssistant()
    
    # Load existing data
    print(assistant.load_data())
    print(assistant.get_status_summary())
    
    print("\n💬 Start chatting (type 'quit' to exit, 'save' to save data):")
    print("=" * 60)
    
    while True:
        try:
            user_input = input(f"\n🧑 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == 'quit':
                print(f"\n👋 {assistant.name}: Goodbye! Don't forget to save your data!")
                break
            elif user_input.lower() == 'save':
                print(assistant.save_data())
                continue
            
            # Process command or chat
            response = assistant.process_command(user_input)
            print(f"\n🤖 {assistant.name}: {response}")
            
        except KeyboardInterrupt:
            print(f"\n\n👋 {assistant.name}: Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
