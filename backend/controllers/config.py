import os
from datetime import timedelta

from dotenv import load_dotenv
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI")

    SECRET_KEY=os.environ.get("SECRET_KEY")
    SECURITY_PASSWORD_SALT=os.environ.get("SECURITY_PASSWORD_SALT")

    JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(
        hours=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES"))
    )

    REDIS_URL=os.environ.get("REDIS_URL")
    CELERY_BROKER_URL=os.environ.get("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND=os.environ.get("CELERY_RESULT_BACKEND")

    CACHE_DEFAULT_TIMEOUT=int(os.environ.get("CACHE_DEFAULT_TIMEOUT"))

    MAIL_HOST=os.environ.get("MAIL_HOST")
    MAIL_PORT=int(os.environ.get("MAIL_PORT"))
    MAIL_USERNAME=os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD")
    MAIL_FROM=os.environ.get("MAIL_FROM")
    MAIL_USE_TLS=os.environ.get("MAIL_USE_TLS").lower()=="true"

    ADMIN_EMAIL=os.environ.get("ADMIN_EMAIL")

    DAILY_REMINDER_HOUR=int(os.environ.get("DAILY_REMINDER_HOUR"))
    DAILY_REMINDER_MINUTE=int(os.environ.get("DAILY_REMINDER_MINUTE"))

    EXPORT_FOLDER=os.environ.get("EXPORT_FOLDER")