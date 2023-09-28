from decouple import config


ONCALL_HOST = config("ONCALL_HOST")
ONCALL_PORT = int(config("ONCALL_PORT"))
ADMIN_USERNAME = config("ADMIN_USERNAME")
ADMIN_PASSWORD = config("ADMIN_PASSWORD")
YAML_FILE_NAME = config("YAML_FILE_NAME")
LOGFILE = config("LOGFILE")
