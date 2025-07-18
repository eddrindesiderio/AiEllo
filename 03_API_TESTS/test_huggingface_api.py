#!/usr/bin/env python3
"""
Test script to verify Hugging Face API key is working
"""

import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment variables
load_dotenv()

print("🔍 Testing Hugging Face API Configuration...")
print("=" * 50)

# Check if API key exists
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE")
print(f"API Key found: {'Yes' if HUGGINGFACE_API_KEY else 'No'}")

if HUGGINGFACE_API_KEY:
    print(f"API Key starts with: {HUGGINGFACE_API_KEY[:10]}...")
    print(f"API Key length: {len(HUGGINGFACE_API_KEY)} characters")
    
    # Test if it's not a placeholder
    if HUGGINGFACE_API_KEY == "your_huggingface_api_key_here":
        print("❌ API key is still a placeholder!")
    else:
        print("✅ API key looks valid (not a placeholder)")
        
        # Try to create client
        try:
            hf_client = InferenceClient(token=HUGGINGFACE_API_KEY)
            print("✅ Hugging Face client created successfully")
            
            # Test a simple API call
            try:
                response = hf_client.chat_completion(
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": "What is 2+2?"}
                    ],
                    model="HuggingFaceH4/zephyr-7b-beta",
                    max_tokens=50,
                    temperature=0.2
                )
                print("✅ API test successful!")
                print(f"Response: {response.choices[0].message.content}")
            except Exception as api_error:
                print(f"❌ API test failed: {api_error}")
                
        except Exception as client_error:
            print(f"❌ Failed to create client: {client_error}")
else:
    print("❌ No Hugging Face API key found in environment")

print("\n" + "=" * 50)
print("💡 If you see issues above:")
print("1. Make sure your .env file has: HUGGINGFACE=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")
print("2. Restart your Discord bot after fixing the .env file")
print("3. Make sure there are no extra spaces or quotes around the API key")
