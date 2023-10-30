from app.config import config
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

DB_URI = f'mysql+aiomysql://{config.DB_USERNAME.value}:{config.DB_PASSWORD.value}@{config.DB_HOST.value}:{str(config.DB_PORT.value)}/{config.DB_NAME.value}'


Engine = create_async_engine(DB_URI,poolclass=NullPool)
Base = declarative_base(Engine)


class PrefixerBase(Base):
    __abstract__ = True
    _the_prefix = config.DB_PREFIX.value

    @declared_attr
    def __tablename__(cls):
        return cls._the_prefix + cls.__incomplete_tablename__
