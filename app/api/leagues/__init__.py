from flask import Blueprint

leagues_bp = Blueprint('leagues', __name__)

# Import routes AFTER blueprint creation
from . import routes  # This line is crucial