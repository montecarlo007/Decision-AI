import requests

def test_admin():
    url = "http://127.0.0.1:8000/admin/"
    try:
        response = requests.get(url, allow_redirects=True)
        print(f"Status Code: {response.status_code}")
        print(f"Final URL: {response.url}")
        if response.status_code == 500:
            print("500 Error Detected!")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_admin()
