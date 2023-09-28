from app import schemas
from app import database
from app import request


def login(oncall_host: str, oncall_port: int, username: str, password: str):
    url = "http://{}:{}/login".format(oncall_host, oncall_port)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "username": username,
        "password": password
    }

    resp = request.post(url=url, headers=headers, data=data)

    resp.raise_for_status()

    resp_data = resp.json()

    user = schemas.oncall.User(**resp_data)
    if not user:
        raise ValueError("The user not created")

    if not resp.cookies or "oncall-auth" not in resp.cookies:
        raise ValueError("The oncall-auth cookie do not exists")

    database.oncall_user = user
    database.oncall_cookie_auth = resp.cookies["oncall-auth"]
