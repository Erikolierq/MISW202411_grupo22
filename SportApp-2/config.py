import secrets

class Config:
    SECRET_KEY = '4b705952c332a2084d6493c748a09f8d9a14dd4cf0f8e766'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///sportapp.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_INCLUDE = ['app.tasks']
    MAIL_SERVER = 'in-v3.mailjet.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = '7d7501ea4a24f7e2e341f9b773453859'
    MAIL_PASSWORD = 'f684413092867141be51061b4de'
