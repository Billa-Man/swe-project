import requests
import json
import os

from dotenv import load_dotenv
load_dotenv()

GOPHISH_API_URL=os.getenv('GOPHISH_API_URL')
GOPHISH_API_KEY=os.getenv('GOPHISH_API_KEY')

def create_campaign(name, sender_email, target_group, email_template_id, url):
    """
    Creates a phishing campaign in GoPhish.
    """
    campaign_data = {
        "name": name,
        "sender_address": sender_email,
        "target_groups": [target_group],
        "email_template": email_template_id,
        "url": url
    }
    response = requests.post(
        f"{GOPHISH_API_URL}campaigns?api_key={GOPHISH_API_KEY}",
        json=campaign_data
    )
    return response.json()

def get_campaigns():
    """
    Retrieves all campaigns from GoPhish.
    """
    response = requests.get(
        f"{GOPHISH_API_URL}campaigns?api_key={GOPHISH_API_KEY}"
    )
    return response.json()

def get_campaign_status(campaign_id):
    """
    Retrieves the status of a specific campaign.
    """
    response = requests.get(
        f"{GOPHISH_API_URL}campaigns/{campaign_id}?api_key={GOPHISH_API_KEY}"
    )
    return response.json()

def get_user_responses(campaign_id):
    response = requests.get(
        f"{GOPHISH_API_URL}results?campaign_id={campaign_id}&api_key={GOPHISH_API_KEY}"
    )
    return response.json()

def get_email_templates():
    """
    Fetches email templates from GoPhish.
    
    Returns:
        list: A list of template objects containing id, name, and content details
    """
    try:
        response = requests.get(
            f"{GOPHISH_API_URL}/templates?api_key={GOPHISH_API_KEY}"
        )
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching email templates: {e}")
        return []

def get_employee_groups():
    """
    Fetches target groups (employee groups) from GoPhish.
    
    Returns:
        list: A list of group objects containing id, name, and members
    """
    try:
        response = requests.get(
            f"{GOPHISH_API_URL}/groups?api_key={GOPHISH_API_KEY}"
        )
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching employee groups: {e}")
        return []

