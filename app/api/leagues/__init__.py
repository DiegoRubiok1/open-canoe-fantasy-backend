from flask import Blueprint

leagues_bp = Blueprint('leagues', __name__)

from . import routes  # noqa