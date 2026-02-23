# firebase_config.py
import os
from dotenv import load_dotenv

load_dotenv()

FIREBASE_CONFIG = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL", ""),
"googleClientId": os.getenv("GOOGLE_CLIENT_ID"),
      # Add Google OAuth credentials (get from Firebase Console)
    # "googleClientSecret": "your-google-client-secret"  # Optional but recommended
}
print("Firebase Config Loaded:", "✅" if FIREBASE_CONFIG["apiKey"] else "❌")
