import requests


def get_token(username: str, password: str, login_url: str) -> str:
    """Retrieve authentication token from the login API."""
    headers = {"Content-Type": "application/json"}
    data = {"username": username, "password": password}

    response = requests.post(login_url, json=data, headers=headers)
    if response.status_code == 200:
        try:
            return response.json().get("data", {}).get("token", "")
        except Exception:
            return ""
    return ""
