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

# Landing Page structure:
#   {
#     id                  : int64
#     name                : string
#     html                : string
#     capture_credentials : bool
#     capture_passwords   : bool
#     modified_date       : string(datetime)
#     redirect_url        : string
#   }


def get_landing_pages():
    """
    Returns a list of landing pages.

    Returns:
        [  
            {
                "id": 1,
                "name": "Example Page",
                "html": "<html><head></head><body>This is a test page</body></html>",
                "capture_credentials": true,
                "capture_passwords": true,
                "redirect_url": "http://example.com",
                "modified_date": "2016-11-26T14:04:40.4130048-06:00"
            }
        ]
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
    }

    try:
        response = requests.get(
            f"{GOPHISH_API_URL}/api/pages/",
            headers=headers,
            verify=False
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting landing pages: {e}")
        return None


def get_landing_page_with_id(id):
    """
    Returns a landing page with the provided ID.
    Returns a 404: Not Found error if the specified template doesn't exist.

    Returns:
        {
            "id": 1,
            "name": "Example Page",
            "html": "<html><head></head><body>This is a test page</body></html>",
            "capture_credentials": true,
            "capture_passwords": true,
            "redirect_url": "http://example.com",
            "modified_date": "2016-11-26T14:04:40.4130048-06:00"
        }
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
    }

    try:
        response = requests.get(
            f"{GOPHISH_API_URL}/api/pages/{id}",
            headers=headers,
            verify=False
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Landing page with ID {id} not found")
        return None
    

def create_landing_page(id, name, html, capture_credentials, 
                        capture_passwords, redirect_url, modified_date):                 
    """
    Creates a landing page.

    Input:
        Landing Page structure
    
    Returns:
        {
            "id": 1,
            "name": "Example Page",
            "html": "<html><head></head><body>This is a test page</body></html>",
            "capture_credentials": true, (to capture credentials)
            "capture_passwords": true,   (to capture passwords as well)
            "redirect_url": "http://example.com",
            "modified_date": "2016-11-26T14:04:40.4130048-06:00"
        }
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
    }

    data = {
            "id" : id,
            "name": name,
            "html": html,
            "capture_credentials": capture_credentials,
            "capture_passwords": capture_passwords,
            "redirect_url": redirect_url,
            "modified_date": modified_date,
        }

    try:
        response = requests.post(
            f"{GOPHISH_API_URL}/api/pages/",
            data=data,
            headers=headers,
            verify=False
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Unable to create landing page: {e}")
        return None
    

def modify_landing_page(id, name, html, capture_credentials, 
                        capture_passwords, redirect_url, modified_date):  
    """
    Modifies an existing landing page.

    Input:
        Landing page structure 
    
    Returns:
        {
            "id": 1,
            "name": "Example Page",
            "html": "<html><head></head><body>This is a test page</body></html>",
            "capture_credentials": true,
            "capture_passwords": true,
            "redirect_url": "http://example.com",
            "modified_date": "2016-11-26T14:04:40.4130048-06:00"
        }
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
    }

    data = {
            "id" : id,
            "name": name,
            "html": html,
            "capture_credentials": capture_credentials,
            "capture_passwords": capture_passwords,
            "redirect_url": redirect_url,
            "modified_date": modified_date,
        }

    try:
        response = requests.put(
            f"{GOPHISH_API_URL}/api/pages/{id}",
            data=data,
            headers=headers,
            verify=False
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Unable to modify landing page. Check if landing page with id: {id} exists: {e}")
        return None


def delete_landing_page(id):
    """
    Deletes a landing page by ID.
    Returns:
    {
        "message": "Page Deleted successfully!",
        "success": true,
        "data": null
    }
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
    }

    try:
        response = requests.delete(
            f"{GOPHISH_API_URL}/api/pages/{id}",
            headers=headers,
            verify=False
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Unable to delete landing page. Check if landing page with id: {id} exists: {e}")
        return None
    
def import_site(include_resources, url):
    """
    Fetches a URL to be later imported as a landing page
    Input:
        include_resources: boolean (Whether or not to create a <base> tag in the resulting HTML to resolve static references (recommended: false))
        content: string (The URL to fetch)
    Return:
        {
            "html": "<html><head>..."
        }
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
    }

    data = {
        "include_resources": include_resources,
        "url": url
    }

    try:
        response = requests.post(
            f"{GOPHISH_API_URL}/api/import/site",
            headers=headers,
            data=data,
            verify=False
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Unable to import site: {e}")
        return None

