from dotenv import load_dotenv
import os

load_dotenv()


def get_github_token():
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        raise EnvironmentError("GITHUB_TOKEN not set in environment variables")
    return token


def get_freshdesk_token():
    token = os.getenv('FRESHDESK_TOKEN')
    if not token:
        raise EnvironmentError("FRESHDESK_TOKEN not set in environment variables")
    return token
