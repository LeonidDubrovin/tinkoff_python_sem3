import json
import time

from starlette.exceptions import HTTPException

from app import schemas
from app import database
from app import utils
from app import logger
from app import request
from app import controllers


def read_user(username: str) -> schemas.oncall.User:
    url = "{}://{}:{}/api/v0/users/{}".format(
        utils.ONCALL_PROTOCOL,
        utils.ONCALL_HOST,
        utils.ONCALL_PORT,
        username
    )

    resp = request.get(url=url)

    if not resp.status_code == 200:
        logger.logger.error(
            "Error while getting User with name '{}'. "
            "status code: {}, text = {}".format(
                username, resp.status_code, resp.text
            )
        )
        raise HTTPException(
            status_code=resp.status_code,
            detail=resp.text,
        )

    user = schemas.oncall.User(**resp.json())

    return user


def create_user(user: schemas.custom.User, team: schemas.custom.Team):
    if not database.oncall_user or not database.oncall_cookie_auth:
        raise ValueError("you should login")

    url = "{}://{}:{}/api/v0/users".format(
        utils.ONCALL_PROTOCOL,
        utils.ONCALL_HOST, utils.ONCALL_PORT
    )

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

    if resp.status_code == 201:
        # почему-то oncall создает пользователя игнорируя некоторые поля
        # по этому приходится обновлять
        new_user = read_user(user.name)
        update_user(new_user, user_oncall_data)
    else:
        if resp.status_code == 422 and "already exists" in resp.text:
            logger.logger.info("User with name '{}' already exists".format(user.name))
        else:
            logger.logger.error(
                "Error while creating User. status code: {}, text = {}".format(
                    resp.status_code, resp.text
                )
            )
            raise HTTPException(
                status_code=resp.status_code,
                detail=resp.text,
            )


def update_user(user: schemas.oncall.User, data: dict):
    url = "{}://{}:{}/api/v0/users/{}".format(
        utils.ONCALL_PROTOCOL,
        utils.ONCALL_HOST,
        utils.ONCALL_PORT,
        user.name
    )

    user_oncall_data = {
        "active": user.active,
        "contacts": user.contacts,
        "full_name": user.full_name,
        "name": user.name,
        "time_zone": user.time_zone,
        "photo_url": user.photo_url
    }

    if 'name' in data:
        user_oncall_data['name'] = data['name']
    if 'full_name' in data:
        user_oncall_data['full_name'] = data['full_name']
    if 'time_zone' in data:
        user_oncall_data['time_zone'] = data['time_zone']
    if 'contacts' in data:
        user_oncall_data['contacts'] = data['contacts']
    if 'active' in data:
        user_oncall_data['active'] = data['active']
    if 'photo_url' in data:
        user_oncall_data['photo_url'] = data['photo_url']

    user_oncall_json = json.dumps(user_oncall_data)

    resp = request.put(url=url, data=user_oncall_json)

    if not resp.status_code == 204:
        logger.logger.error(
            "Error while updating User. status code: {}, text = {}".format(
                resp.status_code, resp.text
            )
        )
        raise HTTPException(
            status_code=resp.status_code,
            detail=resp.text,
        )

    logger.logger.info("Successful update User '{}'.".format(user.name))


def add_duty(duty: schemas.custom.Duty, user: schemas.custom.User, team: schemas.custom.Team):
    url = "{}://{}:{}/api/v0/events".format(utils.ONCALL_PROTOCOL, utils.ONCALL_HOST, utils.ONCALL_PORT)

    duty_time = time.mktime(duty.date.timetuple())

    if duty.role == 'primary':
        duty_time_start = duty_time + utils.DUTY_PRIMARY_START_HOUR * 60 * 60
        duty_time_end = duty_time_start + utils.DUTY_DURATION_HOURS * 60 * 60
    elif duty.role == 'secondary':
        duty_time_start = duty_time + utils.DUTY_SECONDARY_START_HOUR * 60 * 60
        duty_time_end = duty_time_start + utils.DUTY_DURATION_HOURS * 60 * 60
    elif duty.role == 'vacation':
        duty_time_start = duty_time + utils.DUTY_PRIMARY_START_HOUR * 60 * 60
        duty_time_end = duty_time_start + utils.DUTY_DURATION_HOURS * 60 * 60
    else:
        logger.logger.error(
            "Duty '{}' role is unsupported".format(duty.role)
        )
        raise ValueError("Duty '{}' role is unsupported".format(duty.role))

    user_oncall = read_user(user.name)
    team_oncall = controllers.team.read_team(team.name)

    event_data = json.dumps({
        "start": duty_time_start,
        "end": duty_time_end,
        "user": user_oncall.name,
        "team": team_oncall.name,
        "role": duty.role
    })

    headers = {
        'Content-Type': 'application/json'
    }

    resp = request.post(url=url, data=event_data, headers=headers)

    if not resp.status_code == 201:
        logger.logger.error(
            "Error while creating Event. status code: {}, text = {}".format(
                resp.status_code, resp.text
            )
        )
        raise HTTPException(
            status_code=resp.status_code,
            detail=resp.text,
        )
