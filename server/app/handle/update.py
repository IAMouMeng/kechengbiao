from datetime import datetime

from app.utils.system import System
from app.utils.tools import mathYearAndXq, getWeeksInfo

from app.models.students_model import Students
from app.models.students_model import Action as StudentsAction
from app.models.exams_model import Action as ExamsAction

from app.models.courses_mode import Action as CoursesAction


async def updateDbExams(request, userInfo, year, semester):
    year, semester = mathYearAndXq(year, semester)

    system = System()
    system.stuId = userInfo.username
    system.cookie = userInfo.cookie
    stuInfo, stuScore = system.GetScore(year, semester)

    if not stuInfo and not stuScore:
        return False

    await StudentsAction(request).UpdateInfo(
        userInfo,
        Students(
            name=stuInfo["姓名"],
            institute=stuInfo["学院"],
            profession=stuInfo["专业"],
            classname=stuInfo["行政班"]
        )
    )

    await ExamsAction(request).Insert(userInfo.username, year, semester, stuScore)

    return True


async def updateDbCourse(requests, username,cookie):
    system = System()
    system.stuId = username
    system.cookie = cookie

    data = system.GetCourses()

    if not data:
        return False

    weekC2E = {
        "一": "Mon",
        "二": "Tues",
        "三": "Wed",
        "四": "Thur",
        "五": "Fri",
        "六": "Sat",
        "天": "Sun"
    }

    res = {
        "Mon": [],
        "Tues": [],
        "Wed": [],
        "Thur": [],
        "Fri": [],
        "Sat": [],
        "Sun": []
    }
    

    for cours in data:
        try:
            cours[1] = getWeeksInfo(cours[1])
            cours = {
                "name": cours[0],
                "info": cours[1],
                "teacher": cours[2],
                "classroom": cours[3]
            }
            res[weekC2E[cours["info"]["day"]]].append(cours)
        except Exception as e:
            print(e)
        

    await CoursesAction(requests).Insert(username, res)
    return res


async def updateAll(request, username, cookie):
    await StudentsAction(request).Insert(username, cookie)

    userInfo = await StudentsAction(request).Get(username)

    year = int(username[:4])

    date = datetime.now()
    yearNow = date.strftime("%Y")
    monthNow = date.strftime("%M")

    semester = ["2", "1"]

    if (year == yearNow and monthNow >= 6 and monthNow <= 12):
        semester.pop(0)

    while year <= int(yearNow):
        for i in semester:
             await updateDbExams(request, userInfo, str(year),i)
        year = year + 1
        print(year,yearNow)
        

    await StudentsAction(request).UpdateTime(userInfo,"exams")

    await updateDbCourse(request,userInfo.username,userInfo.cookie)
    
    await StudentsAction(request).UpdateTime(userInfo,"courses")