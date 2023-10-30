from app.config import config
from sanic import Sanic
from app.api import *
from app.models import Engine
from app.utils.error import CustomErrorHandler
from contextvars import ContextVar
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

app = Sanic(__name__, error_handler=CustomErrorHandler())


app.config.update(config.__dict__)


_sessionmaker = sessionmaker(Engine, AsyncSession, expire_on_commit=False)

_base_model_session_ctx = ContextVar("session")


@app.middleware("request")
async def inject_session(request):
    request.ctx.session = _sessionmaker()
    request.ctx.session_ctx_token = _base_model_session_ctx.set(
        request.ctx.session)


@app.middleware("response")
async def close_session(request, response):
    if hasattr(request.ctx, "session_ctx_token"):
        _base_model_session_ctx.reset(request.ctx.session_ctx_token)
        await request.ctx.session.close()

app.blueprint(api)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=7800, debug=True, auto_reload=True)