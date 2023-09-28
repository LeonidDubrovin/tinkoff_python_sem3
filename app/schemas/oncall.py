from pydantic import BaseModel, EmailStr


class Contact(BaseModel):
    call: str
    email: EmailStr
    im: str | None = None
    sms: str | None = None
    slack: str | None = None


class UserBase(BaseModel):
    name: str
    full_name: str
    time_zone: str | None = None
    photo_url: str | None = None
    active: bool
    god: bool = False
    csrf_token: str | None = None
    contacts: Contact


class User(UserBase):
    id: int


class UserCreate(UserBase):
    pass
