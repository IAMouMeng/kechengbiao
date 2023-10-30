from sanic.response import json
from time import time

class response:
    
    def response(code,msg,data=None):
        return json({"code":code,"msg":msg,"timestmp":int(round(time() * 1000)),"data":data})
    
    def error(msg="error",code=400):
        return response.response(code=code,msg=msg)
    
    def errorWithData(data="None",msg="error"):
        return response.response(code=400,msg=msg,data=data)
    
    def success(msg="success",code=200):
        return response.response(code=code,msg=msg)
    
    def succWithData(data=None,msg="success"):
        return response.response(code=200,msg="success",data=data)
    