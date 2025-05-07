import requests
import json
import os
import urllib3

from loguru import logger
from datetime import datetime, timedelta

from dotenv import load_dotenv
load_dotenv()

# Suppress insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

GOPHISH_API_URL = os.getenv('GOPHISH_API_URL')
GOPHISH_API_KEY = os.getenv('GOPHISH_API_KEY')

# Docs: https://docs.getgophish.com/api-documentation

# Campaign structure:
# {
#   id                  : int64
#   name                : string
#   created_date        : string(datetime)
#   launch_date         : string(datetime)
#   send_by_date        : string(datetime)
#   completed_date      : string(datetime)
#   template            : Template
#   page                : Page
#   status              : string
#   results             : []Result
#   groups              : []Group
#   timeline            : []Event
#   smtp                : SMTP
#   url                 : string
# }

# The template, page, groups, and smtp objects are all Gophish objects. 
# Their format can be found at their various API endpoints.

# Campaign Event structure:
# Gophish keeps track of every event for a campaign in it's timeline. Each event has the following format:
# {
#   email                : string
#   time                 : string(datetime)
#   message              : string
#   details              : string(JSON)
# }

# The details field is a string containing JSON which contains the raw data about an event 
# (such as credentials that were submitted, user-agent information, and more). 
# The details field has the following format:
# {
#   payload              : object
#   browser              : object
# }

# Campaign Results structure:
# In addition to this, campaign results are maintained in the results attribute. 
# This has a format similar to the members of a Group, in that they have the following structure:
# {
#   id                   : int64
#   first_name           : string
#   last_name            : string
#   position             : string
#   status               : string
#   ip                   : string
#   latitude             : float
#   longitude            : float
#   send_date            : string(datetime)
#   reported             : boolean
# }

def get_campaigns():
    """
    Returns a list of campaigns.

    Returns:
    [
        {
            "id": 1,
            "name": "Example Campaign",
            "created_date": "2018-10-08T15:56:29.48815Z",
            "launch_date": "2018-10-08T15:56:00Z",
            "send_by_date": "0001-01-01T00:00:00Z",
            "completed_date": "0001-01-01T00:00:00Z",
            "template": {
            "id": 1,
            "name": "Example Template",
            "subject": "Click here!",
            "text": "",
            "html": "\u003chtml\u003e\n\u003chead\u003e\n\t\u003ctitle\u003e\u003c/title\u003e\n\u003c/head\u003e\n\u003cbody\u003e\n\u003cp\u003eClick \u003ca href=\"{{.URL}}\"\u003ehere\u003c/a\u003e!\u003c/p\u003e\n{{.Tracker}}\u003c/body\u003e\n\u003c/html\u003e\n",
            "modified_date": "2018-10-08T15:54:56.258392Z",
            "attachments": []
            },
            "page": {
                "id": 1,
                "name": "Example Landing Page",
                "html": "\u003chtml\u003e\u003chead\u003e\n\t\u003ctitle\u003e\u003c/title\u003e\n\u003c/head\u003e\n\u003cbody\u003e\n\u003cp\u003eLanding page HTML\u003c/p\u003e\n\n\n\u003c/body\u003e\u003c/html\u003e",
                "capture_credentials": false,
                "capture_passwords": false,
                "redirect_url": "",
                "modified_date": "2018-10-08T15:55:16.416396Z"
            },
            "status": "In progress",
            "results": [
                {
                    "id": "hoqKYFn",
                    "status": "Email Sent",
                    "ip": "",
                    "latitude": 0,
                    "longitude": 0,
                    "send_date": "2018-10-08T15:56:29.535158Z",
                    "reported": false,
                    "modified_date": "2018-10-08T15:56:29.535158Z",
                    "email": "user@example.com",
                    "first_name": "Example",
                    "last_name": "User",
                    "position": ""
                },
                {
                    "id": "VYrDwtG",
                    "status": "Clicked Link",
                    "ip": "::1",
                    "latitude": 0,
                    "longitude": 0,
                    "send_date": "2018-10-08T15:56:29.548722Z",
                    "reported": false,
                    "modified_date": "2018-10-08T15:56:46.955281Z",
                    "email": "foo@bar.com",
                    "first_name": "Foo",
                    "last_name": "Bar",
                    "position": ""
                }
            ],
            "timeline": [
                {
                    "email": "",
                    "time": "2018-10-08T15:56:29.49172Z",
                    "message": "Campaign Created",
                    "details": ""
                },
                {
                    "email": "user@example.com",
                    "time": "2018-10-08T15:56:29.535158Z",
                    "message": "Email Sent",
                    "details": ""
                },
                {
                    "email": "foo@bar.com",
                    "time": "2018-10-08T15:56:29.548722Z",
                    "message": "Email Sent",
                    "details": ""
                },
                {
                    "email": "foo@bar.com",
                    "time": "2018-10-08T15:56:44.679743Z",
                    "message": "Email Opened",
                    "details": "{\"payload\":{\"rid\":[\"VYrDwtG\"]},\"browser\":{\"address\":\"::1\",\"user-agent\":\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36\"}}"
                },
                {
                    "email": "foo@bar.com",
                    "time": "2018-10-08T15:56:46.955281Z",
                    "message": "Clicked Link",
                    "details": "{\"payload\":{\"rid\":[\"VYrDwtG\"]},\"browser\":{\"address\":\"::1\",\"user-agent\":\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36\"}}"
                }
            ],
            "smtp": {
            "id": 1,
            "interface_type": "SMTP",
            "name": "Example Sending Profile",
            "host": "localhost:1025",
            "from_address": "Test User \u003ctest@test.com\u003e",
            "ignore_cert_errors": true,
            "headers": [],
            "modified_date": "2018-09-04T01:24:21.691924069Z"
            },
            "url": "http://localhost"
        }
    ]
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(
            f"{GOPHISH_API_URL}/campaigns/",
            headers=headers,
            verify=False
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting campaign: {e}")
        return None

def get_campaign_with_id(id):
    """
    Returns a campaign with the provided ID.
    Returns a 404: Not Found error if the specified template doesn't exist.

    Returns:
        {
        "id": 1,
        "name": "Example Campaign",
        "created_date": "2018-10-08T15:56:29.48815Z",
        "launch_date": "2018-10-08T15:56:00Z",
        "send_by_date": "0001-01-01T00:00:00Z",
        "completed_date": "0001-01-01T00:00:00Z",
        "template": {
            "id": 1,
            "name": "Example Template",
            "subject": "Click here!",
            "text": "",
            "html": "\u003chtml\u003e\n\u003chead\u003e\n\t\u003ctitle\u003e\u003c/title\u003e\n\u003c/head\u003e\n\u003cbody\u003e\n\u003cp\u003eClick \u003ca href=\"{{.URL}}\"\u003ehere\u003c/a\u003e!\u003c/p\u003e\n{{.Tracker}}\u003c/body\u003e\n\u003c/html\u003e\n",
            "modified_date": "2018-10-08T15:54:56.258392Z",
            "attachments": []
        },
        "page": {
            "id": 1,
            "name": "Example Landing Page",
            "html": "\u003chtml\u003e\u003chead\u003e\n\t\u003ctitle\u003e\u003c/title\u003e\n\u003c/head\u003e\n\u003cbody\u003e\n\u003cp\u003eLanding page HTML\u003c/p\u003e\n\n\n\u003c/body\u003e\u003c/html\u003e",
            "capture_credentials": false,
            "capture_passwords": false,
            "redirect_url": "",
            "modified_date": "2018-10-08T15:55:16.416396Z"
        },
        "status": "In progress",
        "results": [
            {
            "id": "hoqKYFn",
            "status": "Email Sent",
            "ip": "",
            "latitude": 0,
            "longitude": 0,
            "send_date": "2018-10-08T15:56:29.535158Z",
            "reported": false,
            "modified_date": "2018-10-08T15:56:29.535158Z",
            "email": "user@example.com",
            "first_name": "Example",
            "last_name": "User",
            "position": ""
            },
            {
            "id": "VYrDwtG",
            "status": "Clicked Link",
            "ip": "::1",
            "latitude": 0,
            "longitude": 0,
            "send_date": "2018-10-08T15:56:29.548722Z",
            "reported": false,
            "modified_date": "2018-10-08T15:56:46.955281Z",
            "email": "foo@bar.com",
            "first_name": "Foo",
            "last_name": "Bar",
            "position": ""
            }
        ],
        "timeline": [
            {
            "email": "",
            "time": "2018-10-08T15:56:29.49172Z",
            "message": "Campaign Created",
            "details": ""
            },
            {
            "email": "user@example.com",
            "time": "2018-10-08T15:56:29.535158Z",
            "message": "Email Sent",
            "details": ""
            },
            {
            "email": "foo@bar.com",
            "time": "2018-10-08T15:56:29.548722Z",
            "message": "Email Sent",
            "details": ""
            },
            {
            "email": "foo@bar.com",
            "time": "2018-10-08T15:56:44.679743Z",
            "message": "Email Opened",
            "details": "{\"payload\":{\"rid\":[\"VYrDwtG\"]},\"browser\":{\"address\":\"::1\",\"user-agent\":\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36\"}}"
            },
            {
            "email": "foo@bar.com",
            "time": "2018-10-08T15:56:46.955281Z",
            "message": "Clicked Link",
            "details": "{\"payload\":{\"rid\":[\"VYrDwtG\"]},\"browser\":{\"address\":\"::1\",\"user-agent\":\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36\"}}"
            }
        ],
        "smtp": {
            "id": 1,
            "interface_type": "SMTP",
            "name": "Example Sending Profile",
            "host": "localhost:1025",
            "from_address": "Test User \u003ctest@test.com\u003e",
            "ignore_cert_errors": true,
            "headers": [],
            "modified_date": "2018-09-04T01:24:21.691924069Z"
        },
        "url": "http://localhost"
        }
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
    }

    try:
        response = requests.get(
            f"{GOPHISH_API_URL}/campaigns/{id}",
            headers=headers,
            verify=False
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Campaign with ID {id} not found: {e}")
        return None
    

def create_campaign(name, template, page, smtp, groups, launch_date=None):
    """
    Creates and launches a new campaign.

    Args:
        name (str): Name of the campaign
        template (int): ID of the template to use
        page (int): ID of the landing page to use
        smtp (int): ID of the SMTP profile to use
        groups (list[int]): List of group IDs to target
        launch_date (str, optional): ISO8601 formatted datetime for scheduled launch

    Returns:
        dict: Created campaign details, or None on error
    """
    # 1) Build headers
    headers = {
        "Authorization": GOPHISH_API_KEY,
        "Content-Type": "application/json"
    }

    # 2) Normalize launch_date into full ISO8601 with Z-suffix
    if launch_date:
        # Allow inputs like "2025-05-06T10:54" or full ISO strings
        dt = datetime.fromisoformat(launch_date.replace("Z", "+00:00"))
    else:
        dt = datetime.utcnow()
    launch_iso = dt.replace(microsecond=0).isoformat() + "Z"
    send_by_iso = (dt + timedelta(days=7)).replace(microsecond=0).isoformat() + "Z"

    # 3) Look up actual names from GoPhish
    try:
        tmpl = requests.get(f"{GOPHISH_API_URL}/templates/{template}",
                            headers=headers, verify=False)
        tmpl.raise_for_status()
        tmpl_name = tmpl.json()["name"]

        pg = requests.get(f"{GOPHISH_API_URL}/pages/{page}",
                          headers=headers, verify=False)
        pg.raise_for_status()
        page_name = pg.json()["name"]

        smtp_p = requests.get(f"{GOPHISH_API_URL}/smtp/{smtp}",
                              headers=headers, verify=False)
        smtp_p.raise_for_status()
        smtp_name = smtp_p.json()["name"]

        group_objs = []
        for gid in groups:
            g = requests.get(f"{GOPHISH_API_URL}/groups/{gid}",
                             headers=headers, verify=False)
            g.raise_for_status()
            group_objs.append({"name": g.json()["name"]})
    except requests.HTTPError as e:
        logger.error("Error fetching GoPhish resource names: %s", e)
        return None

    # 4) Assemble payload exactly as the API docs expect:
    #    https://docs.getgophish.com/api-documentation/campaigns#create-campaign :contentReference[oaicite:0]{index=0}
    payload = {
        "name": name,
        "template": {"name": tmpl_name},
        "url": "http://localhost",
        "page": {"name": page_name},
        "smtp": {"name": smtp_name},
        "launch_date": launch_iso,
        "send_by_date": send_by_iso,
        "groups": group_objs
    }

    # 5) Debug log what we’re about to send
    logger.info("Creating campaign with payload:\n%s", json.dumps(payload, indent=2))
    logger.info("POSTing to %s/campaigns/", GOPHISH_API_URL)

    # 6) Send it
    try:
        resp = requests.post(f"{GOPHISH_API_URL}/campaigns/",
                             headers=headers,
                             json=payload,
                             verify=False)
        logger.info("GoPhish response %s: %s", resp.status_code, resp.text)
        resp.raise_for_status()
        return resp.json()
    except requests.HTTPError as e:
        logger.error("Failed to create campaign (%s): %s", resp.status_code, resp.text)
        return None
    
def get_campaign_results(id):
    """
    Gets the results for a campaign.
    You may not always want the full campaign details, including the template, landing page, etc. 
    Instead, you may just want to poll the campaign results for updates. 
    This API endpoint only returns information that's relevant to the campaign results.
    Returns a 404 error if the specified campaign isn't found.
    
    Returns:
        {
        "id": 1,
        "name": "Example Campaign",
        "status": "In progress",
        "results": [
            {
            "id": "hoqKYFn",
            "status": "Email Sent",
            "ip": "",
            "latitude": 0,
            "longitude": 0,
            "send_date": "2018-10-08T15:56:29.535158Z",
            "reported": false,
            "modified_date": "2018-10-08T15:56:29.535158Z",
            "email": "user@example.com",
            "first_name": "Example",
            "last_name": "User",
            "position": ""
            },
            {
            "id": "VYrDwtG",
            "status": "Clicked Link",
            "ip": "::1",
            "latitude": 0,
            "longitude": 0,
            "send_date": "2018-10-08T15:56:29.548722Z",
            "reported": false,
            "modified_date": "2018-10-08T15:56:46.955281Z",
            "email": "foo@bar.com",
            "first_name": "Foo",
            "last_name": "Bar",
            "position": ""
            }
        ],
        "timeline": [
            {
            "email": "",
            "time": "2018-10-08T15:56:29.49172Z",
            "message": "Campaign Created",
            "details": ""
            },
            {
            "email": "user@example.com",
            "time": "2018-10-08T15:56:29.535158Z",
            "message": "Email Sent",
            "details": ""
            },
            {
            "email": "foo@bar.com",
            "time": "2018-10-08T15:56:29.548722Z",
            "message": "Email Sent",
            "details": ""
            },
            {
            "email": "foo@bar.com",
            "time": "2018-10-08T15:56:44.679743Z",
            "message": "Email Opened",
            "details": "{\"payload\":{\"rid\":[\"VYrDwtG\"]},\"browser\":{\"address\":\"::1\",\"user-agent\":\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36\"}}"
            },
            {
            "email": "foo@bar.com",
            "time": "2018-10-08T15:56:46.955281Z",
            "message": "Clicked Link",
            "details": "{\"payload\":{\"rid\":[\"VYrDwtG\"]},\"browser\":{\"address\":\"::1\",\"user-agent\":\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36\"}}"
            }
        ]
        }
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
    }


    try:
        response = requests.get(
            f"{GOPHISH_API_URL}/campaigns/{id}/results",
            headers=headers,
            verify=False
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Unable to fetch campaign results. Check if campaign with id: {id} exists: {e}")
        return None

def get_campaign_summary(id):
    """
    Returns summary information about a campaign.
    There may be cases where you aren't interested in the specific results, but rather want high-level statistics, or a "summary", about a campaign.
    The response includes a stats object which has the following format:
        {
            total            : int
            sent             : int
            opened           : int
            clicked          : int
            submitted_data   : int
            email_reported   : int
        }

    Returns:
        {
            "id": 1,
            "created_date": "2018-10-08T15:56:29.48815Z",
            "launch_date": "2018-10-08T15:56:00Z",
            "send_by_date": "0001-01-01T00:00:00Z",
            "completed_date": "0001-01-01T00:00:00Z",
            "status": "In progress",
            "name": "Example Campaign",
            "stats": {
                "total": 2,
                "sent": 2,
                "opened": 1,
                "clicked": 1,
                "submitted_data": 0,
                "email_reported": 0,
                "error": 0
            }
        }
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
    }

    try:
        response = requests.get(
            f"{GOPHISH_API_URL}/campaigns/{id}/summary",
            headers=headers,
            verify=False
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Unable to get campaign summary. Check if campaign with id: {id} exists: {e}")
        return None
    
def delete_campaign(id):
    """
    Deletes a campaign by ID.
    Returns:
    {
        "message": "Campaign deleted successfully!",
        "success": true,
        "data": null
    }
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
    }

    try:
        response = requests.delete(
            f"{GOPHISH_API_URL}/campaigns/{id}",
            headers=headers,
            verify=False
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Unable to delete campaign. Check if campaign with id: {id} exists: {e}")
        return None
    
def complete_campaign(id):
    """
    Marks a campaign as complete.
    
    Return:
        {
        "message": "Campaign completed successfully!",
        "success": true,
        "data": null
        }
    """

    headers = {
        "Authorization": GOPHISH_API_KEY,
    }

    try:
        response = requests.get(
            f"{GOPHISH_API_URL}/campaigns/{id}/complete",
            headers=headers,
            verify=False
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Unable to mark campaign as complete: {e}")
        return None