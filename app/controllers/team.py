import json

from starlette.exceptions import HTTPException

from app import schemas
from app import database
from app import utils
from app import logger
from app import request


def create_team(team: schemas.custom.Team):
    if not database.oncall_user or not database.oncall_cookie_auth:
        raise ValueError("you should login")

    url = "http://{}:{}/api/v0/teams".format(utils.ONCALL_HOST, utils.ONCALL_PORT)

    team_json = team.model_dump_json()

    resp = request.post(url=url, data=team_json)

    if not resp.status_code == 201:
        if resp.status_code == 422 and "already exists" in resp.text:
            logger.logger.info("Team with name '{}' already exists".format(team.name))
        else:
            raise HTTPException(
                status_code=resp.status_code,
                detail=resp.text,
            )


def add_user(team: schemas.custom.Team, user: schemas.custom.User):
    if not database.oncall_user or not database.oncall_cookie_auth:
        raise ValueError("you should login")

    url = "http://{}:{}/api/v0/teams/{}/users".format(utils.ONCALL_HOST, utils.ONCALL_PORT, team.name)

    data = json.dumps({
        "name": user.name
    })

    resp = request.post(url=url, data=data)

    if not resp.status_code == 201:
        if resp.status_code == 422 and "already in team" in resp.text:
            logger.logger.info("User with name '{}' already in team {}".format(user.name, team.name))
        else:
            raise HTTPException(
                status_code=resp.status_code,
                detail=resp.text,
            )
