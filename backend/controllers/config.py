from datetime import timedelta
class Config:
    SQLALCHEMY_DATABASE_URI="sqlite:///app.db"
    SECRET_KEY="syrup"
    SECURITY_PASSWORD_SALT="mysalt"
    JWT_SECRET_KEY="7c1d9e4a5b2f8c6d3a9e1f7b4c8d2e6a9f3c1b5d7e8a2f4c6b9d1e3f5a7c8e2"
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=2)