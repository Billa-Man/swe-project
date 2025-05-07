import requests
import json
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

# Two roles for Users:

# user: A non-administrative user role. Users with this role can create objects and launch campaigns.
# admin: An administrative user. Users with this role can manage system-wide settings as well as other user accounts within Gophish.

# Users have the following format:
# {
#     id              : int64
#     username        : string
#     role            : Role
#     modified_date   : string(datetime)
# }

# Each role has the following format:
# {
#     name            : string
#     slug            : string
#     description     : string
# }

def get_users():
    """
    Returns a list of all user accounts in Gophish.

    Returns:
        [
            {
                "id": 1,
                "username": "admin",
                "role": {
                "slug": "admin",
                "name": "Admin",
                "description": "System administrator with full permissions"
                }
            }
        ]
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
    }

    try:
        response = requests.get(
            f"{GOPHISH_API_URL}/users/",
            headers=headers,
            verify=False
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting Users: {e}")
        return None


def get_user_with_id(id):
    """
    Returns a user with the given ID.
    Returns a 404: Not Found error if the specified template doesn't exist.

    Returns:
        [
            {
                "id": 1,
                "username": "admin",
                "role": {
                "slug": "admin",
                "name": "Admin",
                "description": "System administrator with full permissions"
                }
            }
        ]
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
    }

    try:
        response = requests.get(
            f"{GOPHISH_API_URL}/users/{id}",
            headers=headers,
            verify=False
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"User with ID {id} not found")
        return None
    

def create_user(role, password, username):                 
    """
    Creates a new user.

    Input:
        Landing Page structure
    
    Returns:
        {
            "id": 2,
            "username": "exampleuser",
            "role": {
                "slug": "user",
                "name": "User",
                "description": "User role with edit access to objects and campaigns"
        }
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
    }

    data = {
            "role": role,
            "password": password,
            "username": username,
        }

    try:
        response = requests.post(
            f"{GOPHISH_API_URL}/users/",
            json=data,
            headers=headers,
            verify=False
        )

        # Log the raw response before attempting to parse JSON
        logger.info("RESULTS")
        logger.info(f"Create profile response status: {response.status_code}")
        logger.info(f"Create profile response headers: {response.headers}")
        logger.info(f"DATA")
        logger.info(f"Create profile raw response: {response.text}")

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Unable to create user: {e}")
        return None
    

def modify_user(id, role, password, username):
    """
    Modifies an existing user.

    Input:
        User format 
    
    Returns:
        {
            "id": 2,
            "username": "exampleuser",
            "role": {
                "slug": "user",
                "name": "User",
                "description": "User role with edit access to objects and campaigns"
        }
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
    }

    data = {
            "id": id,
            "role": role,
            "password": password,
            "username": username,
    }

    try:
        response = requests.put(
            f"{GOPHISH_API_URL}/users/{id}",
            json=data,
            headers=headers,
            verify=False
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Unable to modify user. Check if user with id: {id} exists: {e}")
        return None


def delete_user(id):
    """
    Deletes a user by ID.
    Returns:
    {
        "message": "User Deleted successfully!",
        "success": true,
        "data": null
    }
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
    }

    try:
        response = requests.delete(
            f"{GOPHISH_API_URL}/users/{id}",
            headers=headers,
            verify=False
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Unable to delete user. Check if user with id: {id} exists: {e}")
        return None