import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

print(f"DEBUG: {os.environ.get('DEBUG')}")
print(f"OLLAMA_MODEL: {os.environ.get('OLLAMA_MODEL')}")
print(f"MONGODB_URI: {os.environ.get('MONGODB_URI', 'NOT SET')[:20]}...")
