#!/usr/bin/env python3
"""
Move Files to Organized Folders
Actually moves files from root directory to their organized folders
"""

import os
import shutil
from pathlib import Path

def move_files_to_organized_folders():
    """Move files to their respective organized folders"""
    
    # File mappings - what goes where
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
            "discord_setup_guide.md",
            "get_discord_token_guide.md",
            "invite_bot_to_server.md"
        ],
        
        # API TESTS
        "03_API_TESTS": [
            "test_openrouter_api.py",
            "test_claude_api.py", 
            "test_openai_api.py",
            "test_blackbox_api.py",
            "test_api_connection.py",
            "test_api_key_simple.py",
            "test_bot_connection.py",
            "test_huggingface_api.py"
        ],
        
        # DOCUMENTATION
        "04_DOCUMENTATION": [
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
            "deployment/streamlit_app.py",
            "working_ai.py",
            "simple_ai_chat.py",
            "simple_personal_ai.py",
            "eddrin_personal_ai.py",
            "local_ai_setup.py",
            "ai_agent_builder.py"
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
            "update_discord_token.md"
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
    
    print("📁 MOVING FILES TO ORGANIZED FOLDERS")
    print("=" * 50)
    
    moved_count = 0
    
    for directory, files in file_mappings.items():
        print(f"\n📂 Moving files to {directory}:")
        
        # Ensure directory exists
        os.makedirs(directory, exist_ok=True)
        
        for file_path in files:
            if os.path.exists(file_path):
                try:
                    # Get just the filename
                    filename = os.path.basename(file_path)
                    dest_path = os.path.join(directory, filename)
                    
                    # Move the file (not copy)
                    shutil.move(file_path, dest_path)
                    print(f"   ✅ Moved: {file_path} → {dest_path}")
                    moved_count += 1
                    
                except Exception as e:
                    print(f"   ❌ Error moving {file_path}: {e}")
            else:
                print(f"   ⚠️ Not found: {file_path}")
    
    print(f"\n📊 SUMMARY: Moved {moved_count} files to organized folders")
    return moved_count

def clean_empty_directories():
    """Remove empty directories after moving files"""
    print("\n🧹 Cleaning up empty directories...")
    
    directories_to_check = ["deployment"]
    
    for dir_name in directories_to_check:
        if os.path.exists(dir_name):
            try:
                # Check if directory is empty
                if not os.listdir(dir_name):
                    os.rmdir(dir_name)
                    print(f"   ✅ Removed empty directory: {dir_name}")
                else:
                    remaining_files = os.listdir(dir_name)
                    print(f"   ℹ️ {dir_name} still contains: {remaining_files}")
            except Exception as e:
                print(f"   ⚠️ Could not remove {dir_name}: {e}")

def create_navigation_guide():
    """Create a simple navigation guide"""
    
    guide_content = """# 🗂️ FILE ORGANIZATION COMPLETE!

## 📁 YOUR ORGANIZED STRUCTURE

### 🌟 **01_WORKING_SYSTEMS** ← START HERE!
**Your ready-to-use AI systems:**
- `discord_bot_clean.py` - Working Discord bot
- `streamlit_app_openrouter.py` - Working web app
- `final_ai_system_status.md` - System status
- `complete_ai_system_guide.md` - Usage guide

### 🔧 **02_SETUP_GUIDES**
**Setup and configuration files**

### 🧪 **03_API_TESTS**
**API testing scripts**

### 📚 **04_DOCUMENTATION**
**Guides and documentation**

### 💾 **05_BACKUP_SYSTEMS**
**Alternative AI systems**

### 🔍 **06_TROUBLESHOOTING**
**Debug and troubleshooting**

### 👤 **07_PERSONAL_DATA**
**Personal info and configs**

---

## 🚀 QUICK START

### **Launch Your Working AI:**
```bash
# Discord Bot
python 01_WORKING_SYSTEMS/discord_bot_clean.py

# Web App
streamlit run 01_WORKING_SYSTEMS/streamlit_app_openrouter.py
```

### **Test Commands:**
```
!test
!chat What is 2+2?
!chat Tell me about Eddrin
!hello
!help
```

**Your AI system is organized and ready! 🌟**
"""
    
    with open("NAVIGATION_GUIDE.md", "w", encoding="utf-8") as f:
        f.write(guide_content)
    
    print("✅ Created NAVIGATION_GUIDE.md")

def main():
    """Main function to organize files"""
    print("🗂️ MOVING FILES TO ORGANIZED FOLDERS")
    print("=" * 50)
    
    # Move files to organized folders
    moved_count = move_files_to_organized_folders()
    
    # Clean up empty directories
    clean_empty_directories()
    
    # Create navigation guide
    create_navigation_guide()
    
    print(f"\n🎉 FILE ORGANIZATION COMPLETE!")
    print(f"📊 Moved {moved_count} files to organized folders")
    print("\n📁 Your organized structure:")
    print("   01_WORKING_SYSTEMS/     ← START HERE!")
    print("   02_SETUP_GUIDES/")
    print("   03_API_TESTS/")
    print("   04_DOCUMENTATION/")
    print("   05_BACKUP_SYSTEMS/")
    print("   06_TROUBLESHOOTING/")
    print("   07_PERSONAL_DATA/")
    
    print("\n🚀 Quick Start:")
    print("   python 01_WORKING_SYSTEMS/discord_bot_clean.py")
    print("   streamlit run 01_WORKING_SYSTEMS/streamlit_app_openrouter.py")
    
    print("\n✅ All files are now properly organized! 🌟")

if __name__ == "__main__":
    main()
