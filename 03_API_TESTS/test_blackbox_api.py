#!/usr/bin/env python3
"""
Test BlackBox AI API with different endpoints and formats
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BLACKBOX_API_KEY = os.getenv("BLACKBOX_API_KEY", "sk-BtiFdMb6OKw95pLEGknfhQ")

def test_blackbox_endpoints():
    """Test different BlackBox AI API endpoints and formats"""
    
    print("🔍 Testing BlackBox AI API endpoints...")
    print(f"API Key: {BLACKBOX_API_KEY[:20]}...")
    
    # Test different possible endpoints
    endpoints = [
        "https://api.blackbox.ai/v1/chat/completions",
        "https://api.blackbox.ai/chat/completions", 
        "https://api.blackbox.ai/api/chat",
        "https://www.blackbox.ai/api/chat",
        "https://blackbox.ai/api/chat",
        "https://api.blackboxai.com/v1/chat/completions",
        "https://blackboxai.com/api/chat"
    ]
    
    # Test different request formats
    test_message = "What is 2+2?"
    
    for i, endpoint in enumerate(endpoints, 1):
        print(f"\n🔍 Test {i}: {endpoint}")
        
        # Format 1: OpenAI-style
        try:
            headers = {
                "Authorization": f"Bearer {BLACKBOX_API_KEY}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "blackbox",
                "messages": [
                    {"role": "user", "content": test_message}
                ],
                "max_tokens": 100
            }
            
            response = requests.post(endpoint, headers=headers, json=data, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ SUCCESS: {result}")
                return endpoint, "openai_style"
            else:
                print(f"   ❌ Error: {response.text[:200]}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
        
        # Format 2: Custom BlackBox format
        try:
            data = {
                "messages": [{"role": "user", "content": test_message}],
                "id": "test-123",
                "previewToken": None,
                "userId": None,
                "codeModelMode": True,
                "agentMode": {},
                "trendingAgentMode": {},
                "isMicMode": False,
                "maxTokens": 100,
                "playgroundTopP": 0.9,
                "playgroundTemperature": 0.5,
                "isChromeExt": False,
                "githubToken": None
            }
            
            response = requests.post(endpoint, headers=headers, json=data, timeout=10)
            print(f"   Custom format status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ SUCCESS with custom format: {response.text[:200]}")
                return endpoint, "custom_format"
            else:
                print(f"   ❌ Custom format error: {response.text[:200]}")
                
        except Exception as e:
            print(f"   ❌ Custom format exception: {e}")
    
    print("\n❌ No working endpoint found")
    return None, None

def test_alternative_auth():
    """Test different authentication methods"""
    print("\n🔍 Testing alternative authentication methods...")
    
    endpoint = "https://api.blackbox.ai/v1/chat/completions"
    test_message = "Hello"
    
    # Different auth methods
    auth_methods = [
        {"Authorization": f"Bearer {BLACKBOX_API_KEY}"},
        {"Authorization": f"Token {BLACKBOX_API_KEY}"},
        {"X-API-Key": BLACKBOX_API_KEY},
        {"api-key": BLACKBOX_API_KEY},
        {"blackbox-api-key": BLACKBOX_API_KEY}
    ]
    
    for i, headers in enumerate(auth_methods, 1):
        print(f"\n   Auth method {i}: {list(headers.keys())[0]}")
        
        headers["Content-Type"] = "application/json"
        
        data = {
            "model": "blackbox",
            "messages": [{"role": "user", "content": test_message}],
            "max_tokens": 50
        }
        
        try:
            response = requests.post(endpoint, headers=headers, json=data, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"   ✅ SUCCESS: {response.json()}")
                return headers
            else:
                print(f"   ❌ Error: {response.text[:100]}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    return None

if __name__ == "__main__":
    print("🚀 BlackBox AI API Testing Tool")
    print("=" * 50)
    
    # Test endpoints
    working_endpoint, format_type = test_blackbox_endpoints()
    
    if working_endpoint:
        print(f"\n✅ Found working endpoint: {working_endpoint}")
        print(f"✅ Format: {format_type}")
    else:
        print("\n🔍 Testing alternative authentication...")
        working_auth = test_alternative_auth()
        
        if working_auth:
            print(f"✅ Found working auth: {working_auth}")
        else:
            print("\n❌ BlackBox AI API testing failed")
            print("\n💡 Possible issues:")
            print("1. API key might be invalid or expired")
            print("2. BlackBox AI might use a different API format")
            print("3. API might require registration or different authentication")
            print("4. Service might be temporarily unavailable")
            
            print(f"\n🔧 Your API key: {BLACKBOX_API_KEY}")
            print("Please verify this key is correct and active")
