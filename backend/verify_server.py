import requests
import time
import sys

def verify():
    print("Verifying Backend Health...")
    url = "http://127.0.0.1:7860/api/health"
    try:
        # Retry logic for startup
        for i in range(5):
            try:
                res = requests.get(url)
                if res.status_code == 200:
                    print("✅ Backend is Online")
                    return
            except:
                print(f"Waiting for server... ({i+1}/5)")
                time.sleep(2)
        print("❌ Backend failed to start")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    verify()
