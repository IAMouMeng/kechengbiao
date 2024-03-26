import requests

from sanic.blueprints import Blueprint
from app.utils.response import response
from app.utils.system import System
from app.utils.jwt import protected
from app.models.config_model import Action as ConfigAction


system = Blueprint(name="apiSystem", url_prefix="/system")

@system.route("/config", ["GET"])
@protected()
async def getConfig(request,userinfo):
    data = await ConfigAction(request=request).GetAll()
    
    data = data.scalars()
    
    responseList = {}
    
    for i in data:
        responseList[i.name] = i.value
        
    return response.succWithData(responseList)

