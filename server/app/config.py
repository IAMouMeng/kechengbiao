from enum import Enum

class config(Enum):

    # """GEETEST"""
    # GEETEST_SERVER = 'http://gcaptcha4.geetest.com'
    # GEETEST_ID = '245c0bae797270251913ef4be1f03a6a'
    # GEETEST_KEY = 'cf091b41156d7312f667f76b3a0e6c00'
    # GEETEST_CAPTCHA_URL = f'{GEETEST_SERVER}/validate?captcha_id={GEETEST_ID}'

    """CAPTCHA SERVER"""
    CPATCHA_SERVER = "http://captcha.lnsec.cn"

    """JWT"""
    JWT_KEY = b"\xba\xf2\x75\xc2\x09\x72\xba\x36\x40\xd3\x8c\x63\x50\x65\x27\xec"
    JWT_INDATE = 2592000

    """MYSQL"""
    DB_HOST = '113.31.116.153'
    DB_PORT = 3306
    DB_PREFIX = 'assistant_'
    DB_NAME = 'api_score'
    DB_USERNAME = 'api_score'
    DB_PASSWORD = 'D3i4b3chKK2wBZtH'

# from enum import Enum

# class config(Enum):

#     """GEETEST"""
#     GEETEST_SERVER = 'http://gcaptcha4.geetest.com'
#     GEETEST_ID = '245c0bae797270251913ef4be1f03a6a'
#     GEETEST_KEY = 'cf091b41156d7312f667f76b3a0e6c00'
#     GEETEST_CAPTCHA_URL = f'{GEETEST_SERVER}/validate?captcha_id={GEETEST_ID}'

#     """JWT"""
#     JWT_KEY = b"\xba\xf2\x75\xc2\x09\x72\xba\x36\x40\xd3\x8c\x63\x50\x65\x27\xec"
#     JWT_INDATE = 604800

#     """MYSQL"""
#     DB_HOST = '127.0.0.1'
#     DB_PORT = 3306
#     DB_PREFIX = 'assistant_'
#     DB_NAME = 'score'
#     DB_USERNAME = 'score'
#     DB_PASSWORD = 'w2TKsHaBkYmjnnyN'
    
    