import requests

from sanic.blueprints import Blueprint
from app.utils.response import response
from app.utils.request import AuthParam
from app.utils.system import System
from app.utils.jwt import JwtEncode,protected
from app.models.students_model import Action as StudentsAction
from app.handle.update import updateAll
from app.utils.jwt import JwtDecode


user = Blueprint(name="apiUser", url_prefix="/user")

@user.route("/login", ["POST"])
@AuthParam("username","password","token")
async def captchaAndLogin(request):

    username = request.json["username"]
    password = request.json["password"]
    token = request.json["token"]

    if not username.isdigit() or len(username) != 10:
        return response.error("学号有误")

    try:
        param = {
            "token":token
        }
        res = requests.get(f"{request.app.config.CPATCHA_SERVER.value}/captcha/check",params=param).json()
        if res["code"]:
            return response.error(res["msg"])
    except Exception as e:
        # print(e)
        return response.error("通信失败请重试")
    
    system = System()

    result,msg = system.Login(username,password)

    if not result:
        return response.error(msg)
    
    await updateAll(request,username,system.cookie)
    
    return response.succWithData({"token":JwtEncode({"stuId":username})})


@user.route("/info", ["GET"])
@protected()
async def getUserInfo(request,userInfo):
    return response.succWithData(userInfo.to_dict())


@user.route("/check", ["GET"])
async def checkToken(request):
    userInfo = JwtDecode(request.headers.get("Access-Token"))

    if not userInfo:
        return response.error("请先登录",401)
    
    return response.success()
    