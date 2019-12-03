import os, subprocess

appData = {
    'institution_name' : os.environ.get("INSTITUTION_NAME"),
    'institution_initials':os.environ.get("INSTITUTION_INITIALS"),
    'app_base_url' : os.environ.get("APP_URL"),
    'map_coordinates' : '',
    'country' : os.environ.get("COUNTRY"),
    'email' : os.environ.get("MAIL_USERNAME"),
    'primary_phone' : os.environ.get("PRIMARY_PHONE"),
    'secondary_phone' : '',
    'stateOrCounty' : os.environ.get("STATE_OR_COUNTY"),
    'about' : ''
}


class Config:
    '''
    General configuration parent class
    '''
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    UPLOADED_PHOTOS_DEST = 'app/static/photos'

    # email configurations
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    MAIL_MAX_EMAILS = os.environ.get('')
    MAIL_SUPPRESS_SEND = os.environ.get('')
    MAIL_ASCII_ATTACHMENTS = os.environ.get('')
    SUBJECT_PREFIX = appData['institution_name']
    SQLALCHEMY_TRACK_MODIFICATIONS = True 

    # simplemde confirgurations
    # simplemde  configurations
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True


class ProdConfig(Config):
    '''
    Production configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    # SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    APP_URL = os.environ.get('APP_URL')
    TESTING = False
    MAIL_SUPPRESS_SEND = False
    MAIL_DEBUG = False
    DEBUG = False


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://harryking:bigboy999@localhost/school_sys_test'


class DevConfig(Config):
    '''
    Development configuration child class

    Args:
        Config : the parent configuration class with General configuration settings
    '''
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://harryking:bigboy999@localhost/school_system'
    MAIL_SUPPRESS_SEND = True
    MAIL_DEBUG = True 
    TESTING = True
    DEBUG = True


config_options = {
    'development' : DevConfig,
    'production' : ProdConfig,
    'test' : TestConfig
}