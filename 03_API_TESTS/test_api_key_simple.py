#!/usr/bin/env python3
"""
Simple test to check if Hugging Face API key is working
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("🔍 Testing API Key Configuration...")
print("=" * 50)

# Check environment variable
hf_key = os.getenv("HUGGINGFACE")
print(f"1. API Key found in environment: {'Yes' if hf_key else 'No'}")

if hf_key:
    print(f"2. API Key length: {len(hf_key)} characters")
    print(f"3. API Key starts with: {hf_key[:15]}...")
    print(f"4. API Key ends with: ...{hf_key[-10:]}")
    
    # Test if it's a valid format
    if hf_key.startswith('hf_'):
        print("5. ✅ API Key format looks correct (starts with 'hf_')")
        
        # Try to import and test the client
        try:
            from huggingface_hub import InferenceClient
            print("6. ✅ Successfully imported InferenceClient")
            
            try:
                client = InferenceClient(token=hf_key)
                print("7. ✅ Successfully created InferenceClient")
                
                # Try a simple API call
                try:
                    response = client.chat_completion(
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": "What is 1+1?"}
                        ],
                        model="HuggingFaceH4/zephyr-7b-beta",
                        max_tokens=50,
                        temperature=0.2
                    )
                    print("8. ✅ API call successful!")
                    print(f"   Response: {response.choices[0].message.content}")
                    print("\n🎉 Your Hugging Face API key is working perfectly!")
                    
                except Exception as api_error:
                    print(f"8. ❌ API call failed: {api_error}")
                    print("\n💡 This suggests your API key might be invalid or expired.")
                    
            except Exception as client_error:
                print(f"7. ❌ Failed to create client: {client_error}")
                
        except ImportError as import_error:
            print(f"6. ❌ Failed to import: {import_error}")
            print("   Try: pip install huggingface_hub")
            
    else:
        print("5. ❌ API Key format looks incorrect (should start with 'hf_')")
        
else:
    print("2. ❌ No API key found")
    print("   Make sure your .env file contains: HUGGINGFACE=hf_your_key_here")

print("\n" + "=" * 50)
print("💡 If the API key is not working:")
print("1. Check if it's expired at https://huggingface.co/settings/tokens")
print("2. Generate a new token if needed")
print("3. Make sure it has 'Read' permissions")
print("4. Update your .env file with the new token")
