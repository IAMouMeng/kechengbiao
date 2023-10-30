import jwt
from time import time
from sanic import Request
from functools import wraps
from app.config import config
from app.utils.response import response
from app.models.students_model import Action as StudentsAction


def JwtEncode(payload):
    payload["exp"] = int(time()) + config.JWT_INDATE.value
    return jwt.encode(payload,config.JWT_KEY.value)


def JwtDecode(token):
    try:
        payload = jwt.decode(
            token, 
            config.JWT_KEY.value, 
            algorithms=["HS256"]
        )
        if payload.get("exp") < int(time()):
            return None
        return payload
    except jwt.exceptions.InvalidTokenError:
        return None


def protected():
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            userInfo = JwtDecode(request.headers.get("Access-Token"))
            if not userInfo:
                return response.error("请先登录",401)
            
            stuId = userInfo.get("stuId")
            if not stuId:
                return response.error("请先登录",401)
            
            
            userInfo = await StudentsAction(request).Get(userInfo.get("stuId"))

            if not userInfo:
                return response.error("请先登录",401)
            
            return await func(request,userInfo)
        return wrapper
    return decorator
