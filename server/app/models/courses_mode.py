from time import time, localtime, strftime
from sqlalchemy import Column, Integer, String, DateTime,JSON, select, func

from app.models import PrefixerBase

class Courses(PrefixerBase):

    __incomplete_tablename__ = 'courses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32))
    courses = Column(JSON)
    updatetime = Column(DateTime, default=func.now())
    createtime = Column(DateTime, default=func.now())

    def to_dict(self):
        return {
            "courses": self.courses,
            "updatetime": self.updatetime.strftime('%Y-%m-%d %H:%M:%S'),
            "createtime": self.createtime.strftime('%Y-%m-%d %H:%M:%S')
        }
    

class Action:
    def __init__(self, request) -> None:
        self.request = request
        self.Session = request.ctx.session

    async def Get(self,username):
        stmt = select(Courses).filter_by(username=username)
        result = await self.Session.execute(stmt)
        record = result.scalar()

        if not record:
            return False
        
        return record

    
    async def Insert(self,username,courses):
        stmt = select(Courses).filter_by(username=username)
        result = await self.Session.execute(stmt)
        record = result.scalar()

        if not record:
            self.Session.add(
                Courses(
                    username=username,
                    courses=courses
                )
            )
        else:
            record.courses = courses

        await self.Session.commit()
                
            

