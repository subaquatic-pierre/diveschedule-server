import os
import json

# path to config file outsite django server
home = os.path.expanduser("~")
with open(home + "/etc/diveschedule/config.json") as f:
    config = json.load(f)


class Config:

    DEBUG = config.get("DEBUG")
    SECRET_KEY = config.get("SECRET_KEY")
    DATABASE = config.get("DATABASE")
    NAME = config.get("NAME")
    USER = config.get("USER")
    PASSWORD = config.get("PASSWORD")
    HOST = config.get("HOST")
    PORT = config.get("PORT")
