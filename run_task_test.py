import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'decision.settings')
django.setup()

from apps.content.models import DocumentModel
from apps.content.tasks import process_document_task
from bson import ObjectId
import sys

def run_task_manually():
    # Find a pending document
    doc = DocumentModel.objects(status='pending').first()
    if not doc:
        print("No pending documents found.")
        return
    
    print(f"Processing document: {doc.title} (ID: {doc.id})")
    try:
        # Call the task function directly (not .delay())
        result = process_document_task(str(doc.id))
        print(f"Result: {result}")
        
        # Verify status
        doc.reload()
        print(f"Final Status: {doc.status}")
    except Exception as e:
        print(f"Task Failed: {e}")

if __name__ == "__main__":
    try:
        from dotenv import load_dotenv
        load_dotenv()
        run_task_manually()
    except Exception as e:
        print(f"Initialization Error: {e}")
        sys.exit(1)
