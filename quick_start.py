#!/usr/bin/env python3
"""
Quick Start Script - Launch Your Working AI System
"""

import os
import subprocess
import sys

def main():
    print("🚀 Personal AI Assistant - Quick Start")
    print("=" * 50)
    
    print("\n🌟 Your Working AI Systems:")
    print("1. Discord Bot (OpenRouter Claude)")
    print("2. Web App (OpenRouter Claude)")
    print("3. Exit")
    
    while True:
        choice = input("\n👉 Choose an option (1-3): ").strip()
        
        if choice == "1":
            print("\n🤖 Starting Discord Bot...")
            if os.path.exists("01_WORKING_SYSTEMS/discord_bot_clean.py"):
                subprocess.run([sys.executable, "01_WORKING_SYSTEMS/discord_bot_clean.py"])
            else:
                print("❌ Discord bot file not found!")
            break
            
        elif choice == "2":
            print("\n🌐 Starting Web App...")
            if os.path.exists("01_WORKING_SYSTEMS/streamlit_app_openrouter.py"):
                subprocess.run(["streamlit", "run", "01_WORKING_SYSTEMS/streamlit_app_openrouter.py"])
            else:
                print("❌ Web app file not found!")
            break
            
        elif choice == "3":
            print("\n👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
