from sanic.blueprints import Blueprint
from app.utils.response import response
from app.utils.tools import mathYearAndXq
from app.utils.jwt import protected
from app.models.students_model import Action as StudentsAction
from app.models.exams_model import Action as ExamsAction
from app.models.courses_mode import Action as CoursessAction

from app.handle.update import updateDbExams,updateDbCourse

edu = Blueprint(name="apiEdu", url_prefix="/edu")

@edu.route("/getExamsList", ["GET"])
@protected()
async def getExamsList(request,userInfo):
    year = request.args.get("year")
    semester = request.args.get("xq")

    year,semester = mathYearAndXq(year,semester)
    
    exams = await ExamsAction(request).GetExamInfo(userInfo.username,year,semester)

    return response.succWithData(exams)


@edu.route("/updateExamsList", ["GET"])
@protected()
async def updateExamsList(request,userInfo):
    year = request.args.get("year")
    semester = request.args.get("xq")

    responseUpdate = await updateDbExams(request,userInfo,year,semester)

    if not responseUpdate:
        return response.error("令牌过期",401)
    
    await StudentsAction(request).UpdateTime(userInfo,"exams")
    
    return response.success()


@edu.route("/getCoursesList", ["GET"])
@protected()
async def getCoursesList(request,userInfo):
    coursesList = await CoursessAction(request).Get(userInfo.username)

    if not coursesList:
        coursesList = []
    else:
        coursesList = coursesList.to_dict()

    return response.succWithData(coursesList)

@edu.route("/updateCoursesList", ["GET"])
@protected()
async def updateCoursesList(request,userInfo):

    responseUpdate = await updateDbCourse(request,userInfo.username,userInfo.cookie)

    if not responseUpdate:
        return response.error("更新失败",400)
    
    await StudentsAction(request).UpdateTime(userInfo,"courses")
    
    return response.success()
