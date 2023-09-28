import yaml

from app import utils
from app import schemas
from app import controllers
from app import auth
from app import logger


def get_data_from_yaml_file(filename):
    response = None
    with open(filename, 'r') as file:
        data = yaml.safe_load(file)

        if isinstance(data, dict) and "teams" in data:
            response = data["teams"]

    return response


def main():
    if not auth.is_authorized():
        auth.authorize()

    teams_row = get_data_from_yaml_file(utils.YAML_FILE_NAME)
    if not teams_row:
        raise ValueError("The teams is not parsed")

    teams_custom: [schemas.custom.Team] = []
    for team_row in teams_row:
        team = schemas.custom.Team.model_validate(team_row)
        teams_custom.append(team)

    for team_custom in teams_custom:
        controllers.team.create_team(team_custom)

        for user_custom in team_custom.users:
            controllers.user.create_user(user_custom, team_custom)

            controllers.team.add_user(team=team_custom, user=user_custom)

            controllers.user.add_duty(team=team_custom, user=user_custom)

    logger.logger.info("Successful parsing!")


if __name__ == "__main__":
    main()
