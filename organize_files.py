#!/usr/bin/env python3
"""
File Organization Script
Organizes all AI project files into proper directories
"""

import os
import shutil
from pathlib import Path

def create_directory_structure():
    """Create organized directory structure"""
    
    directories = {
        "01_WORKING_SYSTEMS": "Your working AI systems (USE THESE)",
        "02_SETUP_GUIDES": "Setup and configuration guides", 
        "03_API_TESTS": "API testing scripts",
        "04_DOCUMENTATION": "Documentation and guides",
        "05_BACKUP_SYSTEMS": "Backup and alternative systems",
        "06_TROUBLESHOOTING": "Troubleshooting and debug files",
        "07_PERSONAL_DATA": "Personal information and configs"
    }
    
    print("🗂️ Creating organized directory structure...")
    
    for dir_name, description in directories.items():
        os.makedirs(dir_name, exist_ok=True)
        print(f"   ✅ Created: {dir_name} - {description}")
    
    return directories

def organize_files():
    """Organize files into appropriate directories"""
    
    file_mappings = {
        # WORKING SYSTEMS (Most Important)
        "01_WORKING_SYSTEMS": [
            "deployment/discord_bot_clean.py",
            "deployment/streamlit_app_openrouter.py", 
            "final_ai_system_status.md",
            "complete_ai_system_guide.md"
        ],
        
        # SETUP GUIDES
        "02_SETUP_GUIDES": [
            "setup_env_file.py",
            "setup_ai_project.py",
            "setup_discord_bot.py",
            "openrouter_ai_setup_guide.md",
            "claude_ai_setup_guide.md",
            "blackbox_ai_setup_guide.md",
            "run_streamlit_guide.md",
            "discord_setup_guide.md"
        ],
        
        # API TESTS
        "03_API_TESTS": [
            "test_openrouter_api.py",
            "test_claude_api.py", 
            "test_openai_api.py",
            "test_blackbox_api.py",
            "test_api_connection.py",
            "test_api_key_simple.py",
            "test_bot_connection.py"
        ],
        
        # DOCUMENTATION
        "04_DOCUMENTATION": [
            "README.md",
            "final_working_system_guide.md",
            "discord_commands_guide.md",
            "blackbox_api_analysis.md",
            "advanced_training_guide.md"
        ],
        
        # BACKUP SYSTEMS
        "05_BACKUP_SYSTEMS": [
            "deployment/discord_bot_openai.py",
            "deployment/streamlit_app_openai.py",
            "deployment/discord_bot_blackbox_fixed.py",
            "deployment/streamlit_app_blackbox_fixed.py",
            "deployment/discord_bot_blackbox.py",
            "deployment/streamlit_app_blackbox.py",
            "deployment/discord_bot_claude.py",
            "deployment/streamlit_app_claude.py",
            "deployment/discord_bot_openrouter.py",
            "deployment/discord_bot_final.py",
            "deployment/discord_bot_fixed.py",
            "deployment/discord_bot_simple.py",
            "deployment/discord_bot_message_only.py",
            "deployment/discord_bot_slash.py",
            "deployment/discord_bot.py",
            "deployment/streamlit_app.py"
        ],
        
        # TROUBLESHOOTING
        "06_TROUBLESHOOTING": [
            "debug_api_key.py",
            "debug_discord_bot.py",
            "troubleshoot_discord.py",
            "fix_discord_bot.md",
            "fix_discord_commands_guide.md",
            "fix_huggingface_api_key.md",
            "discord_fix_final.md",
            "update_discord_token.md",
            "invite_bot_to_server.md",
            "get_discord_token_guide.md"
        ],
        
        # PERSONAL DATA
        "07_PERSONAL_DATA": [
            "personal_info.txt",
            "corrected_professional_response.txt",
            "fixed_professional_intro.txt",
            "config.json",
            "config.py",
            "requirements.txt"
        ]
    }
    
    print("\n📁 Organizing files...")
    
    for directory, files in file_mappings.items():
        print(f"\n   📂 {directory}:")
        
        for file_path in files:
            if os.path.exists(file_path):
                # Create subdirectories if needed
                dest_path = os.path.join(directory, os.path.basename(file_path))
                
                try:
                    shutil.copy2(file_path, dest_path)
                    print(f"      ✅ Moved: {file_path} → {dest_path}")
                except Exception as e:
                    print(f"      ❌ Error moving {file_path}: {e}")
            else:
                print(f"      ⚠️ Not found: {file_path}")

def create_main_readme():
    """Create main README with organized structure"""
    
    readme_content = """# 🚀 Personal AI Assistant - Complete System

## 📁 ORGANIZED FILE STRUCTURE

### 🌟 **01_WORKING_SYSTEMS** (START HERE!)
**Your ready-to-use AI systems:**
- `discord_bot_clean.py` - Working Discord bot (OpenRouter Claude)
- `streamlit_app_openrouter.py` - Working web app (OpenRouter Claude)  
- `final_ai_system_status.md` - Complete system status and instructions
- `complete_ai_system_guide.md` - Comprehensive usage guide

### 🔧 **02_SETUP_GUIDES**
**Setup and configuration:**
- `setup_env_file.py` - Environment setup
- `openrouter_ai_setup_guide.md` - OpenRouter setup guide
- `run_streamlit_guide.md` - How to run web apps
- `discord_setup_guide.md` - Discord bot setup

### 🧪 **03_API_TESTS**
**API testing scripts:**
- `test_openrouter_api.py` - Test OpenRouter API
- `test_claude_api.py` - Test Claude API
- `test_openai_api.py` - Test OpenAI API

### 📚 **04_DOCUMENTATION**
**Guides and documentation:**
- `README.md` - This file
- `discord_commands_guide.md` - Discord bot commands
- `blackbox_api_analysis.md` - API analysis

### 💾 **05_BACKUP_SYSTEMS**
**Alternative AI systems:**
- Various Discord bots for different AI providers
- Alternative web apps
- Backup configurations

### 🔍 **06_TROUBLESHOOTING**
**Debug and troubleshooting:**
- Debug scripts
- Troubleshooting guides
- Fix instructions

### 👤 **07_PERSONAL_DATA**
**Personal information and configs:**
- `personal_info.txt` - Eddrin's information
- Configuration files
- Requirements

---

## 🚀 QUICK START

### **1. Use Your Working System:**
```bash
# Discord Bot (WORKING)
python 01_WORKING_SYSTEMS/discord_bot_clean.py

# Web App (WORKING)
streamlit run 01_WORKING_SYSTEMS/streamlit_app_openrouter.py
```

### **2. Test Commands:**
```
!test
!chat What is 2+2?
!chat Tell me about Eddrin
!hello
!help
```

### **3. Access Web App:**
- Open: http://localhost:8501
- Start chatting with Claude 3.5 Sonnet

---

## ✅ SYSTEM STATUS

- **✅ OpenRouter Claude** - WORKING (84 credits)
- **❌ OpenAI GPT** - Quota exceeded (no credits)
- **❌ BlackBox AI** - Budget exceeded

**Use the OpenRouter system - it's working perfectly! 🌟**

---

## 🎯 WHAT YOUR AI CAN DO

- **Programming Help** - HTML, CSS, JavaScript, Python
- **Code Generation** - Complete applications and websites
- **Math & Calculations** - Simple to complex problems
- **Personal Questions** - About Eddrin's background and skills
- **Creative Writing** - Essays, content, professional communication
- **Technical Explanations** - AI, web development, programming concepts

---

## 🏆 RECOMMENDATION

**Use your WORKING OpenRouter system:**
- Claude 3.5 Sonnet is more advanced than GPT-3.5-turbo
- 84 credits available, optimized for maximum usage
- No quota or budget issues
- Professional quality responses

**Your AI assistant is ready to help! 🚀**
"""
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("✅ Created organized README.md")

def create_quick_start_script():
    """Create quick start script"""
    
    script_content = """#!/usr/bin/env python3
\"\"\"
Quick Start Script - Launch Your Working AI System
\"\"\"

import os
import subprocess
import sys

def main():
    print("🚀 Personal AI Assistant - Quick Start")
    print("=" * 50)
    
    print("\\n🌟 Your Working AI Systems:")
    print("1. Discord Bot (OpenRouter Claude)")
    print("2. Web App (OpenRouter Claude)")
    print("3. Exit")
    
    while True:
        choice = input("\\n👉 Choose an option (1-3): ").strip()
        
        if choice == "1":
            print("\\n🤖 Starting Discord Bot...")
            if os.path.exists("01_WORKING_SYSTEMS/discord_bot_clean.py"):
                subprocess.run([sys.executable, "01_WORKING_SYSTEMS/discord_bot_clean.py"])
            else:
                print("❌ Discord bot file not found!")
            break
            
        elif choice == "2":
            print("\\n🌐 Starting Web App...")
            if os.path.exists("01_WORKING_SYSTEMS/streamlit_app_openrouter.py"):
                subprocess.run(["streamlit", "run", "01_WORKING_SYSTEMS/streamlit_app_openrouter.py"])
            else:
                print("❌ Web app file not found!")
            break
            
        elif choice == "3":
            print("\\n👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
"""
    
    with open("quick_start.py", "w", encoding="utf-8") as f:
        f.write(script_content)
    
    print("✅ Created quick_start.py")

def main():
    """Main organization function"""
    print("🗂️ ORGANIZING YOUR AI PROJECT FILES")
    print("=" * 50)
    
    # Create directory structure
    create_directory_structure()
    
    # Organize files
    organize_files()
    
    # Create documentation
    create_main_readme()
    create_quick_start_script()
    
    print("\n🎉 FILE ORGANIZATION COMPLETE!")
    print("\n📁 Your organized structure:")
    print("   01_WORKING_SYSTEMS/     ← START HERE!")
    print("   02_SETUP_GUIDES/")
    print("   03_API_TESTS/")
    print("   04_DOCUMENTATION/")
    print("   05_BACKUP_SYSTEMS/")
    print("   06_TROUBLESHOOTING/")
    print("   07_PERSONAL_DATA/")
    
    print("\n🚀 Quick Start:")
    print("   python quick_start.py")
    print("   OR")
    print("   python 01_WORKING_SYSTEMS/discord_bot_clean.py")
    print("   streamlit run 01_WORKING_SYSTEMS/streamlit_app_openrouter.py")
    
    print("\n✅ Your AI system is now perfectly organized! 🌟")

if __name__ == "__main__":
    main()
