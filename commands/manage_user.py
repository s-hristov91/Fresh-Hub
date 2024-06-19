from services.github_service import get_github_user
from services.freshdesk_service import create_or_update_contact
from data_.models import FreshdeskContact
from data_.database import read_query, insert_query, update_query
from common.config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME


def sync_user(username, subdomain):
    github_user = get_github_user(username)

    freshdesk_contact_name = github_user.name if github_user.name else "No Name Provided"

    freshdesk_contact = FreshdeskContact(
        name=freshdesk_contact_name,
        email=github_user.email,
        unique_external_id=github_user.login,
        job_title=github_user.company,
        twitter_id=github_user.twitter_username,
        address=github_user.location,
        description=f"GitHub Profile: {github_user.html_url}\nBio: {github_user.bio}"
    )
    result = create_or_update_contact(freshdesk_contact, subdomain)

    if "Email is Private or None, can't create a new contact!" in result:
        status = "Failed - No Email"
    elif "Created new contact" in result:
        status = "Created"
    elif "Updated contact" in result:
        status = "Updated"
    else:
        status = "Unknown Status"

    if DB_USER and DB_PASSWORD and DB_HOST and DB_NAME:
        existing_user = read_query("SELECT login FROM github_users WHERE login = ?", (github_user.login,))

        if existing_user:
            update_query(
                "UPDATE github_users SET name = ?, created_at = CURRENT_TIMESTAMP, status = ? WHERE login = ?",
                (github_user.name, status, github_user.login)
            )
        else:
            insert_query(
                "INSERT INTO github_users (login, name, status) VALUES (?, ?, ?)",
                (github_user.login, github_user.name, status)
            )

    return result
