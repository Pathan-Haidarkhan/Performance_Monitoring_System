import os
from datetime import timedelta


class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY', 'f879eb11de7464b6afdceb8f37a39f1de1140c6b0ceeeadf629bc3763d6a0285')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:R%40%40t@localhost/pmsdb"

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', '_p66EhcRssEzNxZBjVdGA_Xt3L6oyTZmPU7LzGWUh04')
    JWT_ACCESS_TOKEN_EXPIRATION = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRATION = timedelta(days=1)

    BOOTSTRAP_SERVE_LOCAL = True

# import secrets
#
# JWT_SECRET_KEY = secrets.token_hex(32)
# JWT_SECRET_KEY = secrets.token_urlsafe(32)
# print(JWT_SECRET_KEY)