from enum import Enum

class config(Enum):

    # """GEETEST"""
    # GEETEST_SERVER = 'http://gcaptcha4.geetest.com'
    # GEETEST_ID = '111111111111111111111'
    # GEETEST_KEY = '111111111111111111111'
    # GEETEST_CAPTCHA_URL = f'{GEETEST_SERVER}/validate?captcha_id={GEETEST_ID}'

    """CAPTCHA SERVER"""
    CPATCHA_SERVER = "http://127.0.0.1"

    """JWT"""
    JWT_KEY = "111111111111111111111"
    JWT_INDATE = 604800

    """MYSQL"""
    DB_HOST = '127.0.0.1'
    DB_PORT = 3306
    DB_PREFIX = 'assistant_'
    DB_NAME = '111111111111111111111'
    DB_USERNAME = '111111111111111111111'
    DB_PASSWORD = '111111111111111111111'

    
