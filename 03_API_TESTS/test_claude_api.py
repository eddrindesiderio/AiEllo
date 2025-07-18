#!/usr/bin/env python3
"""
Test script to verify Claude API key is working
"""

import os
from dotenv import load_dotenv
import anthropic

# Load environment variables
load_dotenv()

print("🔍 Testing Claude API Configuration...")
print("=" * 50)

# Check if API key exists
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
print(f"API Key found: {'Yes' if CLAUDE_API_KEY else 'No'}")

if CLAUDE_API_KEY:
    print(f"API Key starts with: {CLAUDE_API_KEY[:15]}...")
    print(f"API Key length: {len(CLAUDE_API_KEY)} characters")
    
    # Test if it's not a placeholder
    if CLAUDE_API_KEY == "your_claude_api_key_here":
        print("❌ API key is still a placeholder!")
    else:
        print("✅ API key looks valid (not a placeholder)")
        
        # Try to create client
        try:
            claude_client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
            print("✅ Claude client created successfully")
            
            # Test a simple API call
            try:
                response = claude_client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=50,
                    messages=[{"role": "user", "content": "What is 2+2? Just give the answer."}]
                )
                print("✅ API test successful!")
                print(f"Response: {response.content[0].text}")
                
                # Test another question
                print("\n🧪 Testing another question...")
                response2 = claude_client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=100,
                    messages=[{"role": "user", "content": "Explain what AI is in one sentence."}]
                )
                print("✅ Second API test successful!")
                print(f"Response: {response2.content[0].text}")
                
            except Exception as api_error:
                print(f"❌ API test failed: {api_error}")
                print(f"Error type: {type(api_error).__name__}")
                
        except Exception as client_error:
            print(f"❌ Failed to create client: {client_error}")
else:
    print("❌ No Claude API key found in environment")

print("\n" + "=" * 50)
print("💡 If you see issues above:")
print("1. Make sure your .env file has: CLAUDE_API_KEY=7e51498febb040aea6c83823a7fe2efb")
print("2. Restart your Discord bot after fixing the .env file")
print("3. Make sure there are no extra spaces or quotes around the API key")
print("4. Install anthropic package: pip install anthropic")
