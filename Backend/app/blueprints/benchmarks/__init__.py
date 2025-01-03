from flask import Blueprint

benchmarks_bp = Blueprint('benchmarks', __name__, url_prefix='/benchmarks')


from . import routes
