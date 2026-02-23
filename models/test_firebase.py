# test_firebase.py
import sys
import os

# Add parent directory
sys.path.insert(0, os.path.dirname(os.getcwd()))

try:
    from firebase_config import FIREBASE_CONFIG
    print("✅ firebase_config.py imported successfully!")
    print(f"API Key present: {bool(FIREBASE_CONFIG['apiKey'])}")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print(f"Current dir: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    
    # Try direct import
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("firebase_config", "firebase_config.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print("✅ Direct import worked!")
    except Exception as e2:
        print(f"❌ Direct import failed: {e2}")