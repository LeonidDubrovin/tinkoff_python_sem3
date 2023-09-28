from app import database
from app import utils
from app import controllers


def authorize():
    if not database.oncall_user or not database.oncall_cookie_auth:
        controllers.auth.login(
            utils.ONCALL_HOST,
            utils.ONCALL_PORT,
            utils.ADMIN_USERNAME,
            utils.ADMIN_PASSWORD
        )


def is_authorized():
    if database.oncall_user and database.oncall_cookie_auth:
        return True
    return False
