from sanic.handlers import ErrorHandler
from app.utils.response import response


class CustomErrorHandler(ErrorHandler):
    def default(self, request, exception):
        if exception.status_code == 404:
            return response.error("方法不存在",404)
        elif exception.status_code == 500:
            return response.error("系统繁忙，请稍后再试",500)
        elif exception.status_code == 405:
            return response.error("请求方法不被允许",405)
        else:
            return response.error(exception.status_code, "未知错误")
