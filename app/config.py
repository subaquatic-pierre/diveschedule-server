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
