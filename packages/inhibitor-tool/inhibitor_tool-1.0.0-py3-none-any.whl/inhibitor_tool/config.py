import os

AUTH_TOKEN_PATH = os.path.expanduser("~/.auth_token")


def load_config():
    """Load API configuration from auth_token file."""
    if not os.path.exists(AUTH_TOKEN_PATH):
        print(
            f"Error: {AUTH_TOKEN_PATH} not found. Please run `source ~/.auth_token` first."
        )
        exit(1)

    config = {}
    with open(AUTH_TOKEN_PATH, "r") as f:
        for line in f:
            key, value = line.strip().split("=")
            config[key.strip()] = value.strip()

    required_keys = ["username", "password", "login_url", "inhibit_url"]
    if not all(k in config for k in required_keys):
        print(f"Error: {AUTH_TOKEN_PATH} is missing required keys: {required_keys}")
        exit(1)

    return config
