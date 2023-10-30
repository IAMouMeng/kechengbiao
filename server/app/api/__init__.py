from .user import user
from .edu import edu
from sanic.blueprints import Blueprint

blueprints = [
    user,
    edu
]

api = Blueprint.group(*blueprints, url_prefix="/api")
