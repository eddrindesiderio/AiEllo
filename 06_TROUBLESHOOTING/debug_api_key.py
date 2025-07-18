#!/usr/bin/env python3
"""
Debug script to check API key configuration and test Hugging Face API
"""

import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment variables
load_dotenv()

print("🔍 Debugging API Key Configuration...")
print("=" * 60)

# Check both possible API key names
hf_api_key_1 = os.getenv("HUGGINGFACE_API_KEY")
hf_api_key_2 = os.getenv("HUGGINGFACE")

print(f"HUGGINGFACE_API_KEY found: {'Yes' if hf_api_key_1 else 'No'}")
if hf_api_key_1:
    print(f"  Value starts with: {hf_api_key_1[:15]}...")
    print(f"  Length: {len(hf_api_key_1)} characters")

print(f"HUGGINGFACE found: {'Yes' if hf_api_key_2 else 'No'}")
if hf_api_key_2:
    print(f"  Value starts with: {hf_api_key_2[:15]}...")
    print(f"  Length: {len(hf_api_key_2)} characters")

# Use the same logic as the Discord bot
HUGGINGFACE_API_KEY = hf_api_key_1 or hf_api_key_2
print(f"\nFinal API key selected: {'Yes' if HUGGINGFACE_API_KEY else 'No'}")

if HUGGINGFACE_API_KEY:
    print(f"Selected key starts with: {HUGGINGFACE_API_KEY[:15]}...")
    
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
                print("🧪 Testing API call...")
                response = hf_client.chat_completion(
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant. Give short, direct answers."},
                        {"role": "user", "content": "What is 2+2? Just give the answer."}
                    ],
                    model="HuggingFaceH4/zephyr-7b-beta",
                    max_tokens=50,
                    temperature=0.1
                )
                print("✅ API test successful!")
                print(f"Response: {response.choices[0].message.content}")
                
                # Test another question
                print("\n🧪 Testing another question...")
                response2 = hf_client.chat_completion(
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant. Give short, direct answers."},
                        {"role": "user", "content": "Explain basic AI concepts in one sentence."}
                    ],
                    model="HuggingFaceH4/zephyr-7b-beta",
                    max_tokens=100,
                    temperature=0.3
                )
                print("✅ Second API test successful!")
                print(f"Response: {response2.choices[0].message.content}")
                
            except Exception as api_error:
                print(f"❌ API test failed: {api_error}")
                print(f"Error type: {type(api_error).__name__}")
                
        except Exception as client_error:
            print(f"❌ Failed to create client: {client_error}")
            print(f"Error type: {type(client_error).__name__}")
else:
    print("❌ No Hugging Face API key found in environment")

print("\n" + "=" * 60)
print("🔧 Current .env file should contain:")
print("DISCORD_BOT_TOKEN=MTM5NTM5MDk0MjY1OTM0NjU1NA.G07Vdg.HPNZ5_GW3KTw3t22D4euTy_0eCpRRRwe35KSoU")
print("HUGGINGFACE_API_KEY=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")
print("HUGGINGFACE=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")
print("\n💡 If API tests fail:")
print("1. Check if your Hugging Face API key is valid")
print("2. Make sure the model 'HuggingFaceH4/zephyr-7b-beta' is accessible")
print("3. Try a different model if needed")
