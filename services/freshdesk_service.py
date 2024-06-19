import requests
from common.auth import get_freshdesk_token
from data_.models import FreshdeskContact
import base64


def get_freshdesk_headers():
    token = get_freshdesk_token()
    auth_encoded = base64.b64encode(f"{token}:X".encode('utf-8')).decode('utf-8')
    return {
        "Authorization": f"Basic {auth_encoded}",
        "Content-Type": "application/json"
    }

def get_contact_by_id(unique_id, subdomain):
    headers = get_freshdesk_headers()
    url = f"https://{subdomain}.freshdesk.com/api/v2/contacts?unique_external_id={unique_id}"
    response = requests.get(url, headers=headers)

    if response.status_code == 404:
        return None
    response.raise_for_status()
    contacts = response.json()

    if contacts:
        return contacts[0]
    return None


def create_or_update_contact(contact: FreshdeskContact, subdomain):
    existing_contact = get_contact_by_id(contact.unique_external_id, subdomain)
    headers = get_freshdesk_headers()
    url = f"https://{subdomain}.freshdesk.com/api/v2/contacts"
    payload = contact.dict()

    if existing_contact:
        contact_id = existing_contact['id']
        print(f"Updating Freshdesk contact with ID {contact_id} with the following parameters: {payload}")
        response = requests.put(f"{url}/{contact_id}", headers=headers, json=payload)
        response.raise_for_status()
        return f"Updated contact {contact.name} ({contact.email})"
    else:
        if contact.email is None:
            return "Email is Private or None, can't create a new contact!"
        print(f"Creating a new Freshdesk contact with the following parameters: {payload}")
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return f"Created new contact {contact.name} ({contact.email})"

