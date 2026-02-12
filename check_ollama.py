import requests
import sys

def check_ollama():
    base_url = 'http://localhost:11434'
    try:
        # Check if running
        resp = requests.get(base_url, timeout=5)
        if resp.status_code == 200:
            print("Ollama is running.")
        else:
            print(f"Ollama returned status code: {resp.status_code}")
            return False

        # List models
        resp = requests.get(f"{base_url}/api/tags", timeout=5)
        if resp.status_code == 200:
            models = resp.json().get('models', [])
            print(f"Available models: {[m['name'] for m in models]}")
            return True
        else:
            print("Failed to list models.")
            return False

    except requests.ConnectionError:
        print("Error: Ollama is NOT running or not accessible at localhost:11434.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

if __name__ == "__main__":
    if check_ollama():
        sys.exit(0)
    else:
        sys.exit(1)
