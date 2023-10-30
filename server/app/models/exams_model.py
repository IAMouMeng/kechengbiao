from time import time, localtime, strftime
from sqlalchemy import Column, Integer, String, DateTime, select, func

from app.models import PrefixerBase
from app.models.students_model import Students
from app.models.students_model import Action as StudentsAction

class Exams(PrefixerBase):

    __incomplete_tablename__ = 'exams'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32))
    year = Column(String(32))
    semester = Column(String(32))
    exam_code = Column(String(32))
    exam_name = Column(String(32))
    exam_type = Column(String(32))
    exam_score = Column(String(32))
    exam_owner = Column(String(32))
    exam_makeup_score = Column(String(32))
    exam_regrade_score = Column(String(32))
    exam_credit_points = Column(String(32))
    exam_mark_minor = Column(String(32)) 
    exam_gpa = Column(String(32)) 
    updatetime = Column(DateTime, default=func.now())
    createtime = Column(DateTime, default=func.now())

    def to_dict(self):
        return {
            "exam_code": self.exam_code,
            "exam_name": self.exam_name,
            "exam_type": self.exam_type,
            "exam_score": self.exam_score,
            "exam_owner": self.exam_owner,
            "exam_makeup_score": self.exam_makeup_score,
            "exam_regrade_score": self.exam_regrade_score,
            "exam_credit_points": self.exam_credit_points,
            "exam_mark_minor": self.exam_mark_minor,
            "exam_gpa": self.exam_gpa,
            "updatetime": self.updatetime.strftime('%Y-%m-%d %H:%M:%S'),
            "createtime": self.createtime.strftime('%Y-%m-%d %H:%M:%S')
        }
    

class Action:
    def __init__(self, request) -> None:
        self.request = request
        self.Session = request.ctx.session

    async def GetAll(self,username,year,semester):
        stmt = select(Exams).filter_by(username=username,year=year,semester=semester)
        result = await self.Session.execute(stmt)
        return result

    async def GetExamInfo(self,username,year,semester):
        
        stuData = await StudentsAction(self.request).Get(username)
        stuData = stuData.to_dict()


        examData = await self.GetAll(username,year,semester)
        examData = examData.scalars()
        
        examsDict = []

        for exam in examData:
            examsDict.append(exam.to_dict())

        dict = {"student":stuData,"exams":{}}
        dict["exams"]["year"] = year
        dict["exams"]["semester"] = semester
        dict["exams"]["data"] = examsDict
        return dict

    
    async def Insert(self,username,year,semester,examInfo):
        for exam in examInfo:
            stmt = select(Exams).filter_by(exam_code=exam[0],username=username,year=year,semester=semester)
            result = await self.Session.execute(stmt)
            record = result.scalar()

            if not record:
                self.Session.add(
                    Exams(
                        username=username,
                        year = year,
                        semester = semester,
                        exam_code = exam[0],
                        exam_name = exam[1],
                        exam_type = exam[2],
                        exam_score = exam[3],
                        exam_owner = exam[4],
                        exam_makeup_score = exam[5],
                        exam_regrade_score = exam[6],
                        exam_credit_points = exam[7],
                        exam_mark_minor = exam[8],
                        exam_gpa = exam[9],
                    )
                )
            else:
                record.exam_name = exam[1]
                record.exam_type = exam[2]
                record.exam_score = exam[3]
                record.exam_owner = exam[4]
                record.exam_makeup_score = exam[5]
                record.exam_regrade_score = exam[6]
                record.exam_credit_points = exam[7]
                record.exam_mark_minor = exam[8]
                record.exam_gpa = exam[9]
                record.createtime = Exams.createtime

            await self.Session.commit()
                
            

