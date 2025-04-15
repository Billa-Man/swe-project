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
    }

    try:
        response = requests.get(
            f"{GOPHISH_API_URL}/api/campaigns/",
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
            f"{GOPHISH_API_URL}/api/campaigns/{id}",
            headers=headers,
            verify=False
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Campaign with ID {id} not found: {e}")
        return None
    

def create_campaign(id, name, created_date, launch_date, send_by_date, 
                    completed_date, template, page, status, results, groups, 
                    timeline, smtp, url):                 
    """
    Creates and launches a new campaign.

    This method expects the campaign to be provided in JSON format. 
    For the various objects in a campaign, such as the template, landing page, or sending profile, you need to provide the name attribute.

    You can schedule a campaign to launch at a later time. To do this, simply put the desired time you want the campaign to launch in the launch_date attribute. 
    Gophish expects the date to be provided in ISO8601 format.
    Without setting a launch date, Gophish launches the campaign immediately.

    By default, Gophish sends all the emails in a campaign as quickly as possible. 
    Instead, you may wish to spread emails out over a period of minutes, hours, days, or weeks. 
    This is possible by setting the send_by_date to an ISO8601 formatted datetime. 
    It's important to note that this must be after the launch_date.

    Input:
        Campaign Format
    
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
        "timeline": null,
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

    data = {
            "id" : id,
            "name": name,
            "created_date": created_date,
            "launch_date": launch_date,
            "send_by_date": send_by_date,
            "completed_date": completed_date,
            "template": template,
            "page": page,
            "status": status,
            "results": results,
            "groups": groups,
            "timeline": timeline,
            "smtp": smtp,
            "url": url
        }

    try:
        response = requests.post(
            f"{GOPHISH_API_URL}/api/campaigns/",
            data=data,
            headers=headers,
            verify=False
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Unable to create campaign: {e}")
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
            f"{GOPHISH_API_URL}/api/campaigns/{id}/results",
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
            f"{GOPHISH_API_URL}/api/campaigns/{id}/summary",
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
            f"{GOPHISH_API_URL}/api/campaigns/{id}",
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
            f"{GOPHISH_API_URL}/api/campaigns/{id}/complete",
            headers=headers,
            verify=False
        )

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Unable to mark campaign as complete: {e}")
        return None

