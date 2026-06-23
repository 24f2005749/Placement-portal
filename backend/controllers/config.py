from datetime import timedelta
class Config:
    SQLALCHEMY_DATABASE_URI="sqlite:///app.db"
    SECRET_KEY="syrup"
    SECURITY_PASSWORD_SALT="mysalt"
    JWT_SECRET_KEY="mysecret"
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=15)