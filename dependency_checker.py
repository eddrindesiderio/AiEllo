#!/usr/bin/env python3
"""
Comprehensive Dependency Checker for AI Project
Checks all required dependencies and identifies missing packages
"""

import sys
import importlib
import subprocess
import pkg_resources

def print_header():
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                🔍 Dependency Status Checker 🔍               ║
    ║              Identifying Missing Dependencies                ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def check_package(package_name, import_name=None):
    """Check if a package is installed and importable"""
    if import_name is None:
        import_name = package_name
    
    try:
        # Check if package is installed
        pkg_resources.get_distribution(package_name)
        installed = True
        version = pkg_resources.get_distribution(package_name).version
    except pkg_resources.DistributionNotFound:
        installed = False
        version = "Not installed"
    
    try:
        # Check if package is importable
        importlib.import_module(import_name)
        importable = True
    except ImportError as e:
        importable = False
        import_error = str(e)
    
    return {
        'package': package_name,
        'import_name': import_name,
        'installed': installed,
        'version': version,
        'importable': importable,
        'error': import_error if not importable else None
    }

def main():
    print_header()
    
    # Core dependencies to check
    dependencies = [
        ('openai', 'openai'),
        ('anthropic', 'anthropic'),
        ('transformers', 'transformers'),
        ('torch', 'torch'),
        ('tokenizers', 'tokenizers'),
        ('streamlit', 'streamlit'),
        ('gradio', 'gradio'),
        ('flask', 'flask'),
        ('fastapi', 'fastapi'),
        ('uvicorn', 'uvicorn'),
        ('langchain', 'langchain'),
        ('langchain-openai', 'langchain_openai'),
        ('langchain-community', 'langchain_community'),
        ('huggingface-hub', 'huggingface_hub'),
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('requests', 'requests'),
        ('python-dotenv', 'dotenv'),
        ('pydantic', 'pydantic'),
        ('pinecone', 'pinecone'),
        ('chromadb', 'chromadb'),
        ('sentence-transformers', 'sentence_transformers'),
        ('datasets', 'datasets'),
        ('discord.py', 'discord'),
        ('speechrecognition', 'speech_recognition'),
        ('pyttsx3', 'pyttsx3'),
        ('pillow', 'PIL'),
        ('opencv-python', 'cv2'),
        ('jupyter', 'jupyter'),
        ('ipykernel', 'ipykernel')
    ]
    
    print("📋 Checking dependencies...\n")
    
    missing_packages = []
    import_errors = []
    installed_count = 0
    
    for package_name, import_name in dependencies:
        result = check_package(package_name, import_name)
        
        if result['installed'] and result['importable']:
            print(f"✅ {package_name:<25} v{result['version']}")
            installed_count += 1
        elif result['installed'] and not result['importable']:
            print(f"⚠️  {package_name:<25} v{result['version']} (Import Error)")
            import_errors.append((package_name, result['error']))
        else:
            print(f"❌ {package_name:<25} Not installed")
            missing_packages.append(package_name)
    
    print(f"\n📊 Summary:")
    print(f"✅ Installed and working: {installed_count}/{len(dependencies)}")
    print(f"❌ Missing packages: {len(missing_packages)}")
    print(f"⚠️  Import errors: {len(import_errors)}")
    
    if missing_packages:
        print(f"\n❌ Missing Dependencies Detected!")
        print("The following packages need to be installed:")
        for package in missing_packages:
            print(f"   • {package}")
        
        print(f"\n💡 To install missing packages, run:")
        print(f"pip install {' '.join(missing_packages)}")
        
        print(f"\n🚀 Or install all requirements:")
        print(f"pip install -r requirements.txt")
    
    if import_errors:
        print(f"\n⚠️  Import Errors Detected!")
        for package, error in import_errors:
            print(f"   • {package}: {error}")
    
    if not missing_packages and not import_errors:
        print(f"\n🎉 All dependencies are properly installed and working!")
        print(f"You're ready to run your AI applications!")

if __name__ == "__main__":
    main()
