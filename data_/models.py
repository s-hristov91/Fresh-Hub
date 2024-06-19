from pydantic import BaseModel, HttpUrl, EmailStr


class GitHubUser(BaseModel):
    login: str
    name: str | None = None
    company: str | None = None
    location: str | None = None
    email: EmailStr | None = None
    html_url: HttpUrl
    bio: str | None = None
    twitter_username: str | None = None


class FreshdeskContact(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    unique_external_id: str
    job_title: str | None = None
    twitter_id: str | None = None
    address: str | None = None
    description: str | None = None