#!/usr/bin/env python3
"""
Test OpenAI API with your key
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "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")

def test_openai_api():
    """Test OpenAI API with different models and requests"""
    
    print("🔍 Testing OpenAI API...")
    print(f"API Key: {OPENAI_API_KEY[:20]}...")
    
    if not OPENAI_API_KEY:
        print("❌ No OpenAI API key found")
        return False
    
    # Set up OpenAI client
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    # Test different models and requests
    test_cases = [
        {
            "name": "GPT-3.5-turbo (Simple Math)",
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": "What is 2+2?"}
            ],
            "max_tokens": 50
        },
        {
            "name": "GPT-3.5-turbo (Programming)",
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful programming assistant."},
                {"role": "user", "content": "Write a simple Python function to add two numbers."}
            ],
            "max_tokens": 150
        },
        {
            "name": "GPT-4 (if available)",
            "model": "gpt-4",
            "messages": [
                {"role": "user", "content": "Hello, how are you?"}
            ],
            "max_tokens": 50
        }
    ]
    
    successful_tests = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 Test {i}: {test_case['name']}")
        
        try:
            response = client.chat.completions.create(
                model=test_case["model"],
                messages=test_case["messages"],
                max_tokens=test_case["max_tokens"],
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content.strip()
            print(f"   ✅ SUCCESS: {ai_response}")
            successful_tests += 1
            
            # Show usage info if available
            if hasattr(response, 'usage'):
                usage = response.usage
                print(f"   📊 Tokens used: {usage.total_tokens} (prompt: {usage.prompt_tokens}, completion: {usage.completion_tokens})")
            
        except Exception as e:
            print(f"   ❌ FAILED: {e}")
    
    print(f"\n📊 Test Results: {successful_tests}/{len(test_cases)} tests passed")
    
    if successful_tests > 0:
        print("✅ OpenAI API is working!")
        return True
    else:
        print("❌ OpenAI API is not working")
        return False

def test_account_info():
    """Test OpenAI account information"""
    print("\n🔍 Testing OpenAI account information...")
    
    try:
        # Set up client for account info
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Try to get models (this will show if API key is valid)
        models = client.models.list()
        print(f"✅ API key is valid! Found {len(models.data)} available models")
        
        # Show some available models
        gpt_models = [model.id for model in models.data if 'gpt' in model.id.lower()]
        print(f"📋 Available GPT models: {gpt_models[:5]}...")  # Show first 5
        
        return True
        
    except Exception as e:
        print(f"❌ Account info error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 OpenAI API Testing Tool")
    print("=" * 50)
    
    # Test account info first
    account_valid = test_account_info()
    
    if account_valid:
        # Test API calls
        api_working = test_openai_api()
        
        if api_working:
            print("\n🎉 GREAT NEWS!")
            print("✅ Your OpenAI API key is working perfectly!")
            print("✅ You can now use GPT-3.5-turbo and possibly GPT-4")
            print("\n🚀 Ready to run your AI systems:")
            print("   python deployment/discord_bot_openai.py")
            print("   streamlit run deployment/streamlit_app_openai.py")
        else:
            print("\n⚠️ API key is valid but some requests failed")
            print("💡 This might be due to rate limits or model availability")
    else:
        print("\n❌ OpenAI API key issues detected")
        print("💡 Possible problems:")
        print("1. API key might be invalid or expired")
        print("2. Account might not have sufficient credits")
        print("3. API key might not have the right permissions")
        
        print(f"\n🔧 Your API key: {OPENAI_API_KEY}")
        print("Please verify this key is correct and active at https://platform.openai.com/")
