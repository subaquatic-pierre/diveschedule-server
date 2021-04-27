import os
import ast
from pathlib import Path
import json
from sys import path


def get_list(text):
    return [item.strip() for item in text.split(",")]


def get_bool_from_env(name, default_value):
    if name in os.environ:
        value = os.environ[name]
        try:
            return ast.literal_eval(value)
        except ValueError as e:
            raise ValueError("{} is an invalid value for {}".format(value, name)) from e
    return default_value


class Config:
    pass


dev_env = get_bool_from_env("DEV_ENV", False)

if dev_env:
    with open(os.path.join(Path.home(), "etc/diveschedule/config.json"), "r") as f:
        config = json.load(f)

    Config.DEBUG = True
    Config.SECRET_KEY = "supersecret"
    Config.DB_NAME = config.get("DB_NAME")
    Config.DB_USER = config.get("DB_USER")
    Config.DB_PASSWORD = config.get("DB_PASSWORD")
    Config.DB_HOST = config.get("DB_HOST")
    Config.DB_PORT = config.get("DB_PORT")
    Config.EMAIL_URL = config.get("EMAIL_URL")
    Config.ALLOWED_HOSTS = get_list(config.get("ALLOWED_HOSTS"))
    Config.CSRF_TRUSTED_ORIGINS = get_list(config.get("CSRF_TRUSTED_ORIGINS"))
    Config.AWS_MEDIA_BUCKET_NAME = config.get("AWS_MEDIA_BUCKET_NAME")
    Config.AWS_STORAGE_BUCKET_NAME = config.get("AWS_STORAGE_BUCKET_NAME")
    Config.AWS_ACCESS_KEY_ID = config.get("AWS_ACCESS_KEY_ID")

else:
    Config.DEBUG = get_bool_from_env("DEBUG", True)
    Config.SECRET_KEY = os.environ.get("SECRET_KEY")
    Config.DB_NAME = os.environ.get("DB_NAME")
    Config.DB_USER = os.environ.get("DB_USER")
    Config.DB_PASSWORD = os.environ.get("DB_PASSWORD")
    Config.DB_HOST = os.environ.get("DB_HOST")
    Config.DB_PORT = os.environ.get("DB_PORT")
    Config.EMAIL_URL = os.environ.get("EMAIL_URL")
    Config.ALLOWED_HOSTS = get_list(os.environ.get("ALLOWED_HOSTS"))
    Config.CSRF_TRUSTED_ORIGINS = get_list(os.environ.get("CSRF_TRUSTED_ORIGINS"))
    Config.AWS_MEDIA_BUCKET_NAME = os.environ.get("AWS_MEDIA_BUCKET_NAME")
    Config.AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
    Config.AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    Config.AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
