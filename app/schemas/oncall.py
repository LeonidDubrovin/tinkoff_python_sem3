from pydantic import BaseModel, EmailStr


class Contact(BaseModel):
    call: str
    email: EmailStr
    im: str | None = None
    sms: str | None = None
    slack: str | None = None


class UserBase(BaseModel):
    name: str
    full_name: str | None = None
    time_zone: str | None = None
    photo_url: str | None = None
    active: bool
    god: bool = False
    csrf_token: str | None = None
    contacts: Contact | dict | None = None


class User(UserBase):
    id: int


class UserCreate(UserBase):
    pass


class TeamBase(BaseModel):
    name: str
    scheduling_timezone: str
    email: str | None = None
    slack_channel: str | None = None
    slack_channel_notifications: str | None = None
    iris_plan: str | None = None
    iris_enabled: bool | None = None
    override_phone_number: str | None = None
    api_managed_roster: int | None = None
    users: list[User]
    # admins: None
    # services: None
    # rosters: None

class Team(TeamBase):
    id: int


class Event(BaseModel):
    start: int
    end: int
    user: User
    team: Team
    role: str
