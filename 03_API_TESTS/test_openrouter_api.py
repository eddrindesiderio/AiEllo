#!/usr/bin/env python3
"""
Test script to verify OpenRouter API key is working with Claude 3.5 Sonnet
"""

import os
from dotenv import load_dotenv
import aiohttp
import asyncio
import json

# Load environment variables
load_dotenv()

print("🔍 Testing OpenRouter API Configuration...")
print("=" * 50)

# Check if API key exists
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or os.getenv("CLAUDE_API_KEY")
print(f"API Key found: {'Yes' if OPENROUTER_API_KEY else 'No'}")

if OPENROUTER_API_KEY:
    print(f"API Key starts with: {OPENROUTER_API_KEY[:15]}...")
    print(f"API Key length: {len(OPENROUTER_API_KEY)} characters")
    
    # Test if it's not a placeholder
    if OPENROUTER_API_KEY == "your_openrouter_api_key_here":
        print("❌ API key is still a placeholder!")
    else:
        print("✅ API key looks valid (not a placeholder)")
        
        # Test OpenRouter API call
        async def test_openrouter():
            url = "https://openrouter.ai/api/v1/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/your-repo",
                "X-Title": "Personal AI Assistant Test"
            }
            
            data = {
                "model": "anthropic/claude-3.5-sonnet",
                "messages": [
                    {"role": "user", "content": "What is 2+2? Just give the answer."}
                ],
                "max_tokens": 50,
                "temperature": 0.1
            }
            
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, headers=headers, json=data) as response:
                        if response.status == 200:
                            result = await response.json()
                            print("✅ OpenRouter API test successful!")
                            print(f"Response: {result['choices'][0]['message']['content']}")
                            
                            # Test another question
                            print("\n🧪 Testing another question...")
                            data2 = {
                                "model": "anthropic/claude-3.5-sonnet",
                                "messages": [
                                    {"role": "user", "content": "Explain what AI is in one sentence."}
                                ],
                                "max_tokens": 100,
                                "temperature": 0.2
                            }
                            
                            async with session.post(url, headers=headers, json=data2) as response2:
                                if response2.status == 200:
                                    result2 = await response2.json()
                                    print("✅ Second API test successful!")
                                    print(f"Response: {result2['choices'][0]['message']['content']}")
                                else:
                                    error_text = await response2.text()
                                    print(f"❌ Second API test failed: {response2.status} - {error_text}")
                        else:
                            error_text = await response.text()
                            print(f"❌ API test failed: {response.status} - {error_text}")
                            
            except Exception as api_error:
                print(f"❌ API test failed: {api_error}")
                print(f"Error type: {type(api_error).__name__}")
        
        # Run the async test
        try:
            asyncio.run(test_openrouter())
        except Exception as e:
            print(f"❌ Failed to run test: {e}")
            
else:
    print("❌ No OpenRouter API key found in environment")

print("\n" + "=" * 50)
print("💡 If you see issues above:")
print("1. Make sure your .env file has: OPENROUTER_API_KEY=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")
print("2. Restart your Discord bot after fixing the .env file")
print("3. Make sure there are no extra spaces or quotes around the API key")
print("4. Install aiohttp package: pip install aiohttp")
print("5. Check your OpenRouter account has credits/access to Claude models")
