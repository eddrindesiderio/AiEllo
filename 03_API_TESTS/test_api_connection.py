#!/usr/bin/env python3
"""
Test Hugging Face API connection to debug why Discord bot isn't using it
"""

import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import asyncio

# Load environment variables
load_dotenv()

async def test_huggingface_api():
    """Test the Hugging Face API connection"""
    print("🔍 Testing Hugging Face API Connection...")
    print("=" * 60)
    
    # Check API key
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY") or os.getenv("HUGGINGFACE")
    print(f"API Key found: {'Yes' if HUGGINGFACE_API_KEY else 'No'}")
    
    if not HUGGINGFACE_API_KEY:
        print("❌ No API key found!")
        return False
    
    print(f"API Key starts with: {HUGGINGFACE_API_KEY[:15]}...")
    print(f"API Key length: {len(HUGGINGFACE_API_KEY)} characters")
    
    # Test API connection
    try:
        print("\n🧪 Creating Hugging Face client...")
        hf_client = InferenceClient(token=HUGGINGFACE_API_KEY)
        print("✅ Client created successfully")
        
        print("\n🧪 Testing simple API call...")
        
        # Test with a simple message
        messages = [
            {"role": "system", "content": "You are a helpful assistant. Give short, direct answers."},
            {"role": "user", "content": "What is 2+2? Just give the answer."}
        ]
        
        response = await asyncio.to_thread(
            hf_client.chat_completion,
            messages=messages,
            model="HuggingFaceH4/zephyr-7b-beta",
            max_tokens=50,
            temperature=0.1
        )
        
        ai_response = response.choices[0].message.content
        print(f"✅ API Response: {ai_response}")
        
        # Test another question
        print("\n🧪 Testing another question...")
        messages2 = [
            {"role": "system", "content": "You are a helpful assistant. Give short, direct answers."},
            {"role": "user", "content": "Explain what AI is in one sentence."}
        ]
        
        response2 = await asyncio.to_thread(
            hf_client.chat_completion,
            messages=messages2,
            model="HuggingFaceH4/zephyr-7b-beta",
            max_tokens=100,
            temperature=0.3
        )
        
        ai_response2 = response2.choices[0].message.content
        print(f"✅ API Response 2: {ai_response2}")
        
        print("\n✅ Hugging Face API is working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ API Error: {e}")
        print(f"Error type: {type(e).__name__}")
        
        # Try different model
        try:
            print("\n🔄 Trying different model...")
            response3 = await asyncio.to_thread(
                hf_client.chat_completion,
                messages=[{"role": "user", "content": "Hello"}],
                model="microsoft/DialoGPT-medium",
                max_tokens=50
            )
            print("✅ Alternative model works!")
            return True
        except Exception as e2:
            print(f"❌ Alternative model also failed: {e2}")
            return False

if __name__ == "__main__":
    asyncio.run(test_huggingface_api())
