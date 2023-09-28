from starlette.exceptions import HTTPException

from app import schemas
from app import database
from app import utils
from app import logger
from app import request


def create_user(user: schemas.custom.User, team: schemas.custom.Team):
    if not database.oncall_user or not database.oncall_cookie_auth:
        raise ValueError("you should login")

    url = "http://{}:{}/api/v0/users".format(utils.ONCALL_HOST, utils.ONCALL_PORT)

    user_oncall_data = {
        "active": 1,
        "contacts": {
            "call": user.phone_number,
            "email": user.email
        },
        "full_name": user.full_name,
        "name": user.name,
        "time_zone": team.scheduling_timezone
    }

    user_oncall = schemas.oncall.UserCreate(**user_oncall_data)
    user_oncall_json = user_oncall.model_dump_json()

    resp = request.post(url=url, data=user_oncall_json)

    if not resp.status_code == 201:
        if resp.status_code == 422 and "already exists" in resp.text:
            logger.logger.info("User with name '{}' already exists".format(user.name))
        else:
            raise HTTPException(
                status_code=resp.status_code,
                detail=resp.text,
            )


def add_duty():
    pass
