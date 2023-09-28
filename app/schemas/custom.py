from pydantic import BaseModel, validator
from datetime import datetime


class Duty(BaseModel):
    date: datetime
    role: str

    @validator("date", pre=True)
    def parse_birthdate(cls, value):
        return datetime.strptime(
            value,
            "%d/%m/%Y"
        ).date()


class User(BaseModel):
    name: str
    full_name: str
    phone_number: str
    email: str
    duty: list[Duty]


class Team(BaseModel):
    name: str
    scheduling_timezone: str
    email: str | None
    slack_channel: str | None
    users: list[User] | None = None



