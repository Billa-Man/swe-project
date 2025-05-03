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

# Sending profile structure:
# {
#   id                 : int64
#   name               : string
#   username           : string (optional)
#   password           : string (optional)
#   host               : string
#   interface_type     : string
#   from_address       : string
#   ignore_cert_errors : boolean (default:false)
#   modified_date      : string(datetime)
#   headers            : array({key: string, value: string}) (optional)
# }

def get_sending_profiles():
    """
    Gets a list of the sending profiles created by the authenticated user.

    Returns:
    [
        {
            "id" : 1,
            "name":"Example Profile",
            "interface_type":"SMTP",
            "from_address":"John Doe <john@example.com>",
            "host":"smtp.example.com:25",
            "username":"",
            "password":"",
            "ignore_cert_errors":true,
            "modified_date": "2016-11-20T14:47:51.4131367-06:00",
            "headers": [
            {
                "key": "X-Header",
                "value": "Foo Bar"
            }
            ]
        }
    ]
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(
            f"{GOPHISH_API_URL}/smtp/",
            headers=headers,
            verify=False
        )

        response.raise_for_status()
        logger.info(f"Response status: {response.status_code}")
        logger.info(f"Response content: {response.text}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting sending profiles: {e}")
        if hasattr(e, 'response') and e.response:
            logger.error(f"Response status: {e.response.status_code}")
            logger.error(f"Response content: {e.response.text}")
        return None

def get_sending_profile_with_id(id):
    """
    Returns a sending profile given an ID, 
    returning a 404 error if no sending profile with the provided ID is found.

    Returns:
       {
            "id" : 1,
            "name":"Example Profile",
            "interface_type":"SMTP",
            "from_address":"John Doe <john@example.com>",
            "host":"smtp.example.com:25",
            "username":"",
            "password":"",
            "ignore_cert_errors":true,
            "modified_date": "2016-11-20T14:47:51.4131367-06:00",
            "headers": [
                {
                "key": "X-Header",
                "value": "Foo Bar"
                }
            ]
        } 
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(
            f"{GOPHISH_API_URL}/smtp/{id}",
            headers=headers,
            verify=False
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Sending profile with ID {id} not found")
        return None
    
def create_sending_profile(name, host, interface_type, from_address, modified_date
                           , ignore_cert_errors, username, password, profile_headers=[]):
    
    """
    Creates a sending profile.

    Input:
        {
            id                 : int64
            name               : string
            username           : string (optional)
            password           : string (optional)
            host               : string
            interface_type     : string
            from_address       : string
            ignore_cert_errors : boolean (default:false)
            modified_date      : string(datetime)
            headers            : array({key: string, value: string}) (optional)
        }
    
    Returns:
        {
            "id" : 1,
            "name":"Example Profile",
            "interface_type":"SMTP",
            "from_address":"John Doe <john@example.com>",
            "host":"smtp.example.com:25",
            "username":"",
            "password":"",
            "ignore_cert_errors":true,
            "modified_date": "2016-11-20T14:47:51.4131367-06:00",
            "headers": [
                {
                "key": "X-Header",
                "value": "Foo Bar"
                }
            ]
        }
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
    }

    data = {
            "name": name,
            "interface_type": interface_type,
            "from_address": from_address,
            "host": host,
            "username": username,
            "password": password,
        }

    try:
        response = requests.post(
            f"{GOPHISH_API_URL}/smtp/",
            json=data,
            headers=headers,
            verify=False,
        )
        
        # Log the raw response before attempting to parse JSON
        logger.info("RESULTS")
        logger.info(f"Create profile response status: {response.status_code}")
        logger.info(f"Create profile response headers: {response.headers}")
        logger.info(f"DATA")
        logger.info(f"Create profile raw response: {response.text}")
        
        # Only try to parse JSON if the content type is application/json
        if 'application/json' in response.headers.get('Content-Type', ''):
            result = response.json()
            return result
        else:
            logger.error(f"Server returned non-JSON response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Unable to create a sending profile: {e}")
        if hasattr(e, 'response') and e.response:
            logger.error(f"Response status: {e.response.status_code}")
            logger.error(f"Response content: {e.response.text}")
        return None
    except ValueError as e:  # This catches JSON parsing errors
        logger.error(f"JSON parsing error: {e}")
        logger.error(f"Response content that failed to parse: {response.text}")
        return None
    
def modify_sending_profile(id, name, host, interface_type, from_address, modified_date
                           , ignore_cert_errors=True, username="", password="", profile_headers=None):
    """
    Modifies an existing sending profile.

    Input:
        {
            id                 : int64
            name               : string
            username           : string (optional)
            password           : string (optional)
            host               : string
            interface_type     : string
            from_address       : string
            ignore_cert_errors : boolean (default:false)
            modified_date      : string(datetime)
            headers            : array({key: string, value: string}) (optional)
        }
    
    Returns:
        {
            "id" : 1,
            "name":"Example Profile",
            "interface_type":"SMTP",
            "from_address":"John Doe <john@example.com>",
            "host":"smtp.example.com:25",
            "username":"",
            "password":"",
            "ignore_cert_errors":true,
            "modified_date": "2016-11-20T14:47:51.4131367-06:00",
            "headers": [
                {
                "key": "X-Header",
                "value": "Foo Bar"
                }
            ]
        }
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
        "Content-Type": "application/json",
    }

    data = {
            "id" : id,
            "name": name,
            "interface_type": interface_type,
            "from_address": from_address,
            "host": host,
            "username": username,
            "password": password,
            "ignore_cert_errors": ignore_cert_errors,
            "modified_date": modified_date,
            "headers": profile_headers,
        }

    try:
        response = requests.put(
            f"{GOPHISH_API_URL}/smtp/{id}",
            json=data,
            headers=headers,
            verify=False
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Unable to modify sending profile. Check if sending profile with id: {id} exists: {e}")
        return None

def delete_sending_profile(id):
    """
    Deletes a sending profile by ID.
    Returns:
    {
        "message": "SMTP deleted successfully!",
        "success": true,
        "data": null
    }
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
    }

    try:
        response = requests.delete(
            f"{GOPHISH_API_URL}/smtp/{id}",
            headers=headers,
            verify=False
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Unable to delete sending profile. Check if sending profile with id: {id} exists: {e}")
        return None