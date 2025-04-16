import requests
import os
import urllib3

from loguru import logger

from dotenv import load_dotenv
load_dotenv()

# Suppress insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

GOPHISH_API_URL = os.getenv('GOPHISH_API_URL')
GOPHISH_API_KEY = os.getenv('GOPHISH_API_KEY')

# Docs: https://docs.getgophish.com/api-documentation

def reset_api_key():
    """
    This allows you to reset your API key to a new, randomly generated key.
    This method requires you to authenticate using your existing API key.

    Returns:
        {
            "success": true,
            "message": "API Key successfully reset!",
            "data": "0123456789abcdef"
        }
    """
    headers = {
        "Authorization": GOPHISH_API_KEY,
    }

    try:
        response = requests.post(
            f"{GOPHISH_API_URL}/reset",
            headers=headers,
            verify=False
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error resetting API key: {e}")
        return None