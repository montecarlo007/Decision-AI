
import os
import django
from mongoengine import connect, disconnect
from django.conf import settings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'decision.settings')
django.setup()

from apps.users.models import User
from django.contrib.sessions.models import Session

def verify_setup():
    print("--- Verifying MongoDB Connection ---")
    try:
        # Check connection
        # settings.MONGO_URI is used in settings.py
        print(f"MongoDB URI from settings: {settings.MONGO_URI}")
        # Try to count users
        user_count = User.objects.count()
        print(f"Connection successful. User count: {user_count}")
        
        if user_count > 0:
            print("Users found:")
            for user in User.objects.all():
                print(f" - {user.email} (Role: {user.role}, Is Active: {user.is_active})")
        else:
            print("No users found. You may need to register a user.")

    except Exception as e:
        print(f"ERROR connecting to MongoDB: {e}")

    print("\n--- Verifying Django Sessions (SQLite) ---")
    try:
        # Check if session table exists by trying to access it
        session_count = Session.objects.count()
        print(f"Session table exists. Current active sessions: {session_count}")
    except Exception as e:
        print(f"ERROR accessing Django Sessions (likely missing migrations): {e}")

if __name__ == "__main__":
    verify_setup()
