import requests
import datetime
import sys
from inhibitor_tool.auth import get_token
from inhibitor_tool.config import load_config
from inhibitor_tool.utils import validate_content
from inhibitor_tool.constants import MAX_TTL


def inhibit(content: str, ttl: int):
    """Send an inhibition request with the given content and TTL."""
    if not validate_content(content):
        print(
            "Error: Inhibition content must be at least 10 characters and cannot contain spaces."
        )
        sys.exit(1)

    if ttl > MAX_TTL:
        print(f"Error: TTL cannot exceed {MAX_TTL} hours.")
        sys.exit(1)

    config = load_config()
    username, password, login_url, inhibit_url = (
        config["username"],
        config["password"],
        config["login_url"],
        config["inhibit_url"],
    )

    token = get_token(username, password, login_url)
    if not token:
        print("Error: Unable to retrieve authentication token.")
        sys.exit(1)

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    name = f"cli_{username}_{timestamp}"

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "type": 1,
        "state": 0,
        "maskAlarmType": "content",
        "policyStartTime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "durationUnit": "h",
        "name": name,
        "maskContent": content,
        "duration": str(ttl),
        "remark": "Inhibition request via CLI",
    }

    response = requests.post(inhibit_url, headers=headers, json=data, verify=False)

    if response.status_code == 200:
        print("Success: Inhibition request sent.")
    else:
        print(
            f"Error: Failed to send inhibition request. Status code: {response.status_code}, Response: {response.text}"
        )
