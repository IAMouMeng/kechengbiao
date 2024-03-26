import datetime
from app.models import PrefixerBase
from sqlalchemy import Column, Integer, String, DateTime, select, func


class Config(PrefixerBase):

    __incomplete_tablename__ = 'config'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    value = Column(String(255))
    

class Action:
    def __init__(self, request) -> None:
        self.Session = request.ctx.session

    async def GetAll(self):
        stmt = select(Config)
        result = await self.Session.execute(stmt)
        return result

