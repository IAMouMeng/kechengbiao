from enum import Enum

class config(Enum):

    """CAPTCHA SERVER"""
    CPATCHA_SERVER = "http://captcha.lnsec.cn"
    
    """JWT"""
    JWT_KEY = b"\x66\x66\x66\x66\x66\x66\x66\x66\x66\x66\x66\x66\x66\x66\x66\x66"
    JWT_INDATE = 2592000

    """MYSQL"""
    DB_HOST = '127.0.0.1'
    DB_PORT = 3306
    DB_PREFIX = 'assistant_'
    DB_NAME = 'SearchScore'
    DB_USERNAME = 'SearchScore'
    DB_PASSWORD = 'SearchScore'