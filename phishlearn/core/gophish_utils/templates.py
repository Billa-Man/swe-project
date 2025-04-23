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

# Template structure:
#     {
#     id            : int64
#     name          : string
#     subject       : string
#     text          : string
#     html          : string
#     modified_date : string(datetime)
#     attachments   : list(attachment)
#     }

# Attachments structure:
#   content: string (base64 encoded)
#   type   : string
#   name   : string

def get_templates():
    """
    Returns a list of templates.

    Returns:
        [
            {
                "id" : 1,
                "name" : "Password Reset Template",
                "subject" : "{{.FirstName}}, please reset your password.",
                "text" : "Please reset your password here: {{.URL}}",
                "html" : "<html><head></head><body>Please reset your password <a href\"{{.URL}}\">here</a></body></html>",
                "modified_date" : "2016-11-21T18:30:11.1477736-06:00",
                "attachments" : [],
            }
        ]
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
    }

    try:
        response = requests.get(
            f"{GOPHISH_API_URL}/templates",
            headers=headers,
            verify=False
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting templates: {e}")
        return None

def get_template_with_id(id):
    """
    Returns a template with the provided ID.
    Returns a 404: Not Found error if the specified template doesn't exist.

    Returns:
        {
            "id" : 1,
            "name" : "Password Reset Template",
            "subject" : "{{.FirstName}}, please reset your password.",
            "text" : "Please reset your password here: {{.URL}}",
            "html" : "<html><head></head><body>Please reset your password <a href\"{{.URL}}\">here</a></body></html>",
            "modified_date" : "2016-11-21T18:30:11.1477736-06:00",
            "attachments" : [],
        } 
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
    }

    try:
        response = requests.get(
            f"{GOPHISH_API_URL}/templates/{id}",
            headers=headers,
            verify=False
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Template with ID {id} not found")
        return None
    
def create_template(id, name, subject, text, html, modified_date, attachments):                 
    """
    Creates a sending profile.

    Input:
        Template structure
        Attachments structure 
    
    Returns:
        {
            "id" : 1,
            "name" : "Password Reset Template",
            "subject" : "{{.FirstName}}, please reset your password.",
            "text" : "Please reset your password here: {{.URL}}",
            "html" : "<html><head></head><body>Please reset your password <a href\"{{.URL}}\">here</a></body></html>",
            "modified_date" : "2016-11-21T18:30:11.1477736-06:00",
            "attachments" : [],
        }
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
    }

    data = {
            "id" : id,
            "name": name,
            "subject": subject,
            "text": text,
            "html": html,
            "modified_date": modified_date,
            "attachments": attachments,
        }

    try:
        response = requests.post(
            f"{GOPHISH_API_URL}/templates/",
            data=data,
            headers=headers,
            verify=False
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Unable to create template: {e}")
        return None
    
def modify_template(id, name, subject, text, html, modified_date, attachments):
    """
    Modifies an existing sending profile.

    Input:
        Template structure
        Attachments structure 
    
    Returns:
        {
            "id" : 1,
            "name" : "Password Reset Template",
            "subject" : "{{.FirstName}}, please reset your password.",
            "text" : "Please reset your password here: {{.URL}}",
            "html" : "<html><head></head><body>Please reset your password <a href\"{{.URL}}\">here</a></body></html>",
            "modified_date" : "2016-11-21T18:30:11.1477736-06:00",
            "attachments" : [],
        }
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
    }

    data = {
            "id" : id,
            "name": name,
            "subject": subject,
            "text": text,
            "html": html,
            "modified_date": modified_date,
            "attachments": attachments,
        }

    try:
        response = requests.put(
            f"{GOPHISH_API_URL}/templates/{id}",
            data=data,
            headers=headers,
            verify=False
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Unable to modify template. Check if template with id: {id} exists: {e}")
        return None

def delete_template(id):
    """
    Deletes a sending profile by ID.
    Returns:
    {
        "message": "Template deleted successfully!",
        "success": true,
        "data": null
    }
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
    }

    try:
        response = requests.delete(
            f"{GOPHISH_API_URL}/templates/{id}",
            headers=headers,
            verify=False
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Unable to delete template. Check if template with id: {id} exists: {e}")
        return None
    
def import_email(convert_links, content):
    """
    Imports an email as a template.
    Input:
        convert_links: boolean (Whether or not to convert the links within the email to  automatically.)
        content: string (The original email content in RFC 2045 format, including the original headers.)
    Return:
        {
            "text": "Email text",
            "html": "Email HTML",
            "subject": "Email subject"
        }
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
    }

    data = {
        "convert_links": convert_links,
        "content": content
    }

    try:
        response = requests.post(
            f"{GOPHISH_API_URL}/import/email",
            headers=headers,
            data=data,
            verify=False
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Unable to import email: {e}")
        return None

