import os
import django
from mongoengine import connect
from dotenv import load_dotenv

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'decision.settings')
load_dotenv()
django.setup()

from apps.users.models import User

def create_admin():
    email = "admin@decisionai.com"
    password = "admin1234"
    
    # Connect based on env
    mongo_uri = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/decision_db')
    connect(host=mongo_uri, tlsAllowInvalidCertificates=True)
    
    user = User.objects(email=email).first()
    if user:
        print(f"User {email} already exists. Updating password and role to admin.")
    else:
        print(f"Creating new admin user: {email}")
        user = User(email=email)
        
    user.set_password(password)
    user.role = 'admin'
    user.first_name = "System"
    user.last_name = "Admin"
    user.save()
    print("Admin user created/updated successfully!")

if __name__ == "__main__":
    create_admin()
