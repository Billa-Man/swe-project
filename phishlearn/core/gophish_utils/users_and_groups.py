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

# Group format:
#   {
#       id              : int64
#       name            : string
#       targets         : array(Target)
#       modified_date   : string(datetime)
#   }

# Each recipient in the targets field has the following format:
# {
#     email           : string
#     first_name      : string
#     last_name       : string
#     position        : string
# }

def get_groups():
    """
    Returns a list of templates.

    Returns:
    [
        {
            "id": 1,
            "name": "Example Group",
            "modified_date": "2018-10-08T15:56:13.790016Z",
            "targets": [
            {
                "email": "user@example.com",
                "first_name": "Example",
                "last_name": "User",
                "position": ""
            },
            {
                "email": "foo@bar.com",
                "first_name": "Foo",
                "last_name": "Bar",
                "position": ""
            }
            ]
        }
    ]
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
    }

    try:
        response = requests.get(
            f"{GOPHISH_API_URL}/groups/",
            headers=headers,
            verify=False
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting groups: {e}")
        return None

def get_group_with_id(id):
    """
    Returns a group with the provided ID.
    Returns a 404: Not Found error if the specified template doesn't exist.

    Returns:
        {
            "id": 1,
            "name": "Example Group",
            "modified_date": "2018-10-08T15:56:13.790016Z",
            "targets": [
                {
                "email": "user@example.com",
                "first_name": "Example",
                "last_name": "User",
                "position": ""
                },
                {
                "email": "foo@bar.com",
                "first_name": "Foo",
                "last_name": "Bar",
                "position": ""
                }
            ]
        }
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
    }

    try:
        response = requests.get(
            f"{GOPHISH_API_URL}/groups/{id}",
            headers=headers,
            verify=False
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Group with ID {id} not found")
        return None
    
def get_groups_summary():
    """
    Returns a summary of each group.

    Returns:
        [
            {
                "id": 1,
                "name": "Example Group",
                "modified_date": "2018-10-08T15:56:13.790016Z",
                "num_targets": 2
            }
        ]
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
    }

    try:
        response = requests.get(
            f"{GOPHISH_API_URL}/groups/summary",
            headers=headers,
            verify=False
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting groups: {e}")
        return None

def get_group_summary_with_id(id):
    """
    Returns a summary for a group with the provided ID.
    Returns a 404: Not Found error if the specified template doesn't exist.

    Returns:
        {
            "id": 1,
            "name": "Example Group",
            "modified_date": "2018-10-08T15:56:13.790016Z",
            "num_targets": 2
        }
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
    }

    try:
        response = requests.get(
            f"{GOPHISH_API_URL}/groups/{id}/summary",
            headers=headers,
            verify=False
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Group summary with ID {id} not found")
        return None
    
    
def create_group(id, name, modified_date, targets):                 
    """
    Creates a sending profile.
    When creating a new group, you must specify a unique name, as well as a list of targets.

    Input:
        Group format
        Recipients format
    
    Returns:
        {
            "id": 1,
            "name": "Example Group",
            "modified_date": "2018-10-08T15:56:13.790016Z",
            "targets": [
                {
                "email": "user@example.com",
                "first_name": "Example",
                "last_name": "User",
                "position": ""
                },
                {
                "email": "foo@bar.com",
                "first_name": "Foo",
                "last_name": "Bar",
                "position": ""
                }
            ]
        }
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
    }

    data = {
            "id" : id,
            "name": name,
            "modified_date": modified_date,
            "targets": targets,
        }

    try:
        response = requests.post(
            f"{GOPHISH_API_URL}/groups/",
            json=data,
            headers=headers,
            verify=False
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Unable to create group: {e}")
        return None
    
def modify_group(id, name, modified_date, targets):
    """
    Modifies an existing group.
    The request must include the complete group JSON, not just the fields you're wanting to update. 
    This means that you need to include the matching id field.

    Input:
        Group format
        Recipients format
    
    Returns:
        {
            "id": 1,
            "name": "Example Modified Group",
            "modified_date": "2018-10-08T15:56:13.790016Z",
            "targets": [
                {
                "email": "foo@bar.com",
                "first_name": "Foo",
                "last_name": "Bar",
                "position": ""
                }
            ]
        }
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
    }

    data = {
            "id" : id,
            "name": name,
            "modified_date": modified_date,
            "targets": targets,
        }

    try:
        response = requests.put(
            f"{GOPHISH_API_URL}/groups/{id}",
            json=data,
            headers=headers,
            verify=False
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Unable to modify group. Check if group with id: {id} exists: {e}")
        return None

def delete_group(id):
    """
    Deletes a group by ID.
    Returns:
    {
        "message": "Group deleted successfully!",
        "success": true,
        "data": null
    }
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
    }

    try:
        response = requests.delete(
            f"{GOPHISH_API_URL}/groups/{id}",
            headers=headers,
            verify=False
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Unable to delete group. Check if group with id: {id} exists: {e}")
        return None
    
def import_group(file):
    """
    Imports an email as a template.
    Input:
        file: object (A file upload containing the CSV content to parse.)
    Return:
        [
            {
                "email": "foobar@example.com",
                "first_name": "Example",
                "last_name": "User",
                "position": "Systems Administrator"
            },
            {
                "email": "johndoe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "position": "CEO"
            }
        ]
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
    }

    data = {
        "file": file,
    }

    try:
        response = requests.post(
            f"{GOPHISH_API_URL}/import/group",
            headers=headers,
            json=data,
            verify=False
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Unable to import group: {e}")
        return None

