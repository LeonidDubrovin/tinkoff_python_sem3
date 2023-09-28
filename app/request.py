import requests

from app import database


def post(url: str, data, headers=None):
    if not headers:
        default_headers = {
            'Content-Type': 'application/json',
            'x-csrf-token': database.oncall_user.csrf_token,
            'Cookie': f'oncall-auth={database.oncall_cookie_auth}'
        }
        headers = default_headers

    resp = requests.post(
        url=url, headers=headers, data=data
    )

    return resp
