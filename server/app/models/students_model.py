import datetime
from app.models import PrefixerBase
from sqlalchemy import Column, Integer, String, DateTime, select, func


class Students(PrefixerBase):

    __incomplete_tablename__ = 'students'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32))
    name = Column(String(32))
    institute = Column(String(32))
    profession = Column(String(32))
    classname = Column(String(32))
    avatar = Column(String(32),default="https://static.lnsec.cn/20230930/avatar.png")
    cookie = Column(String(32))
    courses_updatetime = Column(DateTime)
    exams_updatetime = Column(DateTime)
    updatetime = Column(DateTime, default=func.now())
    createtime = Column(DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            "username": self.username,
            "name": self.name,
            "institute": self.institute,
            "profession": self.profession,
            "classname": self.classname,
            "avatar": self.avatar,
            "courses_updatetime": self.courses_updatetime.strftime('%Y-%m-%d %H:%M:%S') if self.courses_updatetime else None,
            "exams_updatetime": self.exams_updatetime.strftime('%Y-%m-%d %H:%M:%S') if self.exams_updatetime else None,
            "updatetime": self.updatetime.strftime('%Y-%m-%d %H:%M:%S'),
            "createtime": self.createtime.strftime('%Y-%m-%d %H:%M:%S')
        }
    

class Action:
    def __init__(self, request) -> None:
        self.Session = request.ctx.session

    async def Get(self,username):
        stmt = select(Students).filter_by(username=username)
        result = await self.Session.execute(stmt)
        record = result.scalar()

        if not record:
            return False
        
        return record

    async def Insert(self, username, cookie):
        async with self.Session.begin():

            record = await self.Get(username)

            if not record:
                self.Session.add(Students(username=username, cookie=cookie))
            else:
                record.cookie = cookie
                record.createtime = Students.createtime

            await self.Session.commit()
    
    async def UpdateTime(self,record,type):
        time = datetime.datetime.now()

        if type == "courses":
            record.courses_updatetime = time
        
        if type == "exams":
            record.exams_updatetime = time
            
        await self.Session.commit()
    
    async def UpdateInfo(self, record,stuInfo):
        record.name = stuInfo.name
        record.classname = stuInfo.classname
        record.institute = stuInfo.institute
        record.profession = stuInfo.profession
        record.createtime = Students.createtime

        await self.Session.commit()
                
            

