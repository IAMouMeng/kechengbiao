from .user import user
from .edu import edu
from .system import system

from sanic.blueprints import Blueprint

blueprints = [
    user,
    edu,
    system
]

api = Blueprint.group(*blueprints, url_prefix="/api")
