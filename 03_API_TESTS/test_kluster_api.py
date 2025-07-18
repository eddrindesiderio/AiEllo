#!/usr/bin/env python3
"""
Test Kluster.ai API
API Key: fbe91b74-c433-4e7f-aaa2-0a1ed9b055ad
"""

import requests
import json

def test_kluster_api():
    """Test Kluster.ai API with the provided key"""
    
    api_key = "fbe91b74-c433-4e7f-aaa2-0a1ed9b055ad"
    
    print("🚀 Testing Kluster.ai API")
    print("=" * 50)
    print(f"🔑 API Key: {api_key}")
    
    # Test different possible endpoints
    endpoints_to_test = [
        "https://api.kluster.ai/v1/chat/completions",
        "https://kluster.ai/api/v1/chat/completions", 
        "https://api.kluster.ai/chat/completions",
        "https://kluster.ai/api/chat/completions"
    ]
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    test_message = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "What is 2+2?"}
        ],
        "max_tokens": 50
    }
    
    for endpoint in endpoints_to_test:
        print(f"\n🔍 Testing endpoint: {endpoint}")
        
        try:
            response = requests.post(endpoint, headers=headers, json=test_message, timeout=10)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ SUCCESS!")
                print(f"Response: {json.dumps(result, indent=2)}")
                return endpoint, True
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
    
    print("\n⚠️ All endpoints failed. Let me try alternative approaches...")
    
    # Try with different models
    models_to_test = ["claude-3", "gpt-4", "gpt-3.5-turbo", "claude-3.5-sonnet"]
    
    for model in models_to_test:
        print(f"\n🔍 Testing with model: {model}")
        test_message["model"] = model
        
        try:
            response = requests.post("https://api.kluster.ai/v1/chat/completions", 
                                   headers=headers, json=test_message, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ SUCCESS with model {model}!")
                print(f"Response: {json.dumps(result, indent=2)}")
                return "https://api.kluster.ai/v1/chat/completions", True
            else:
                print(f"❌ Failed with {model}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Exception with {model}: {e}")
    
    return None, False

if __name__ == "__main__":
    endpoint, success = test_kluster_api()
    
    if success:
        print(f"\n🎉 Kluster.ai API is working!")
        print(f"✅ Working endpoint: {endpoint}")
    else:
        print(f"\n❌ Kluster.ai API test failed")
        print("💡 Will create fallback system")
