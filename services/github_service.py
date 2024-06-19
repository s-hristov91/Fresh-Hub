import requests
from common.auth import get_github_token
from data_.models import GitHubUser


def get_github_user(username: str) -> GitHubUser:
    token = get_github_token()

    url = f"https://api.github.com/users/{username}"
    headers = {
        'Authorization': f'token {token}'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    return GitHubUser(
        login=data['login'],
        name=data.get('name'),
        company=data.get('company'),
        location=data.get('location'),
        email=data.get('email'),
        html_url=data.get('html_url'),
        bio=data.get('bio'),
        twitter_username=data.get('twitter_username')
    )