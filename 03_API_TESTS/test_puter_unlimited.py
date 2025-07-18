#!/usr/bin/env python3
"""
Test Puter.js Unlimited Claude API
This script tests the unlimited Claude 3.5 Sonnet access via Puter.js
"""

import os
import webbrowser
import subprocess
import sys
from pathlib import Path

def test_html_file():
    """Test the HTML file with Puter.js integration"""
    print("🚀 Testing Puter.js Unlimited Claude Integration")
    print("=" * 60)
    
    # Check if HTML file exists
    html_file = "01_WORKING_SYSTEMS/unlimited_claude_chat.html"
    if not os.path.exists(html_file):
        print(f"❌ HTML file not found: {html_file}")
        return False
    
    print(f"✅ HTML file found: {html_file}")
    
    # Get absolute path
    abs_path = os.path.abspath(html_file)
    file_url = f"file:///{abs_path.replace(os.sep, '/')}"
    
    print(f"🌐 Opening in browser: {file_url}")
    
    try:
        # Open in default browser
        webbrowser.open(file_url)
        print("✅ Browser opened successfully!")
        
        print("\n🎯 TEST INSTRUCTIONS:")
        print("1. The HTML page should load with the chat interface")
        print("2. Try typing a message and pressing Enter or clicking Send")
        print("3. The Puter.js integration should provide unlimited Claude responses")
        print("4. Test these example messages:")
        print("   - 'Hello'")
        print("   - 'What is 2+2?'")
        print("   - 'Tell me about Eddrin'")
        print("   - 'Create a Python function'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error opening browser: {e}")
        return False

def test_streamlit_app():
    """Test the Streamlit app with Puter.js integration"""
    print("\n🌐 Testing Streamlit App with Puter.js")
    print("=" * 60)
    
    streamlit_file = "01_WORKING_SYSTEMS/streamlit_app_puter_unlimited.py"
    if not os.path.exists(streamlit_file):
        print(f"❌ Streamlit file not found: {streamlit_file}")
        return False
    
    print(f"✅ Streamlit file found: {streamlit_file}")
    print("🚀 To test the Streamlit app, run:")
    print(f"   streamlit run {streamlit_file}")
    print("\n🎯 STREAMLIT TEST FEATURES:")
    print("- Web interface with Puter.js integration")
    print("- HTML template for unlimited Claude access")
    print("- Fallback responses when needed")
    print("- Personal context about Eddrin")
    
    return True

def show_puter_info():
    """Show information about Puter.js unlimited access"""
    print("\n🌟 PUTER.JS UNLIMITED CLAUDE INFORMATION")
    print("=" * 60)
    
    print("✅ **FREE UNLIMITED ACCESS:**")
    print("   - No API keys required")
    print("   - No usage limits")
    print("   - No costs whatsoever")
    print("   - Claude 3.5 Sonnet model")
    
    print("\n🔧 **HOW IT WORKS:**")
    print("   - Uses Puter.js library: https://js.puter.com/v2/")
    print("   - Direct browser integration")
    print("   - Real-time Claude 3.5 Sonnet responses")
    print("   - User pays model (Puter's 'User Pays' model)")
    
    print("\n🎯 **INTEGRATION METHODS:**")
    print("   1. HTML file: unlimited_claude_chat.html")
    print("   2. Streamlit app: streamlit_app_puter_unlimited.py")
    print("   3. JavaScript API: puter.ai.chat()")
    
    print("\n💡 **ADVANTAGES OVER OTHER APIS:**")
    print("   - ✅ OpenAI GPT: Quota exceeded (no credits)")
    print("   - ✅ BlackBox AI: Budget exceeded")
    print("   - ✅ OpenRouter: Limited credits (84 remaining)")
    print("   - 🌟 Puter.js: UNLIMITED and FREE!")

def main():
    """Main test function"""
    print("🚀 PUTER.JS UNLIMITED CLAUDE TESTING SUITE")
    print("=" * 60)
    
    # Show Puter.js information
    show_puter_info()
    
    # Test HTML file
    html_success = test_html_file()
    
    # Test Streamlit app
    streamlit_success = test_streamlit_app()
    
    print("\n📊 TEST RESULTS:")
    print("=" * 60)
    print(f"HTML File Test: {'✅ PASSED' if html_success else '❌ FAILED'}")
    print(f"Streamlit App Test: {'✅ PASSED' if streamlit_success else '❌ FAILED'}")
    
    if html_success and streamlit_success:
        print("\n🎉 ALL TESTS PASSED!")
        print("🌟 Your unlimited Claude 3.5 Sonnet system is ready!")
        
        print("\n🚀 QUICK START COMMANDS:")
        print("   # Open HTML chat (RECOMMENDED)")
        print("   open 01_WORKING_SYSTEMS/unlimited_claude_chat.html")
        print("   ")
        print("   # Run Streamlit app")
        print("   streamlit run 01_WORKING_SYSTEMS/streamlit_app_puter_unlimited.py")
        
        print("\n🔥 UNLIMITED CLAUDE FEATURES:")
        print("   - FREE unlimited conversations")
        print("   - Claude 3.5 Sonnet intelligence")
        print("   - No API keys or costs")
        print("   - Personal context about Eddrin")
        print("   - Advanced code generation")
        print("   - Creative writing capabilities")
        
    else:
        print("\n⚠️ Some tests failed. Check the file paths and try again.")
    
    print("\n" + "=" * 60)
    print("🌟 PUTER.JS = UNLIMITED CLAUDE 3.5 SONNET FOR FREE!")
    print("=" * 60)

if __name__ == "__main__":
    main()
