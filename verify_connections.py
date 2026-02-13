import os
import sys

# specific to pymongo[srv] requirement
try:
    import pymongo
    from pymongo.errors import ConnectionFailure, ConfigurationError
except ImportError:
    print("Error: pymongo is not installed. Please run 'pip install pymongo[srv]'")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("Error: requests is not installed. Please run 'pip install requests'")
    sys.exit(1)

def load_env(env_path):
    if not os.path.exists(env_path):
        return {}
    env_vars = {}
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    return env_vars

def check_mongodb(uri):
    print(f"Checking MongoDB connection...")
    # Hide password in logs
    safe_uri = uri.split('@')[-1] if '@' in uri else uri
    print(f"Target: ...@{safe_uri}")
    
    try:
        client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000, tlsAllowInvalidCertificates=True)
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
        print("✅ MongoDB connection SUCCESS")
        return True
    except (ConnectionFailure, ConfigurationError) as e:
        print(f"❌ MongoDB connection FAILED: {e}")
        return False
    except Exception as e:
        print(f"❌ MongoDB error: {e}")
        return False

def check_ollama(base_url):
    print(f"Checking Ollama connection...")
    print(f"Target: {base_url}")
    try:
        # Try to get version or tags
        response = requests.get(f"{base_url}/api/tags", timeout=2)
        if response.status_code == 200:
            print("✅ Ollama connection SUCCESS")
            return True
        else:
            print(f"⚠️ Ollama connection returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Ollama connection FAILED (Is Ollama running?)")
        return False
    except Exception as e:
        print(f"❌ Ollama error: {e}")
        return False

def main():
    env_path = os.path.join(os.getcwd(), '.env')
    print(f"Loading environment from {env_path}")
    env = load_env(env_path)
    
    mongo_uri = env.get('MONGODB_URI')
    ollama_url = env.get('OLLAMA_BASE_URL')
    
    if mongo_uri:
        check_mongodb(mongo_uri)
    else:
        print("⚠️ MONGODB_URI not found in .env")
        
    if ollama_url:
        check_ollama(ollama_url)
    else:
        print("⚠️ OLLAMA_BASE_URL not found in .env")

if __name__ == "__main__":
    main()
