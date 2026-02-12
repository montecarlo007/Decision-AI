import os
import django
from mongoengine import connect
from dotenv import load_dotenv

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'decision.settings')
load_dotenv()
django.setup()

from apps.users.models import User

def update_role(email, new_role):
    # Connect based on env
    mongo_uri = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/decision_db')
    connect(host=mongo_uri)
    
    user = User.objects(email=email).first()
    if user:
        user.role = new_role
        user.save()
        print(f"Successfully updated {email} to role: {new_role}")
    else:
        print(f"User {email} not found.")

if __name__ == "__main__":
    update_role("rsovovov@gmail.com", "user")
